"""Explicit provider-receiving checks for ArgDigest #49 / SMonitor #59.

Run this module explicitly against the selected provider. Its filename keeps
the unreleased correction out of ordinary tests against historical providers;
there are no skips or version/implementation probes in this receiving gate.
"""

import json
import warnings
from contextlib import nullcontext

import pytest
import smonitor
from smonitor.handlers.memory import MemoryHandler

from argdigest import DigestConfig, DigestValueError, arg_digest
from argdigest.core.context import Context


class PrivateValue:
    def __init__(self):
        self.conversions = 0

    def __repr__(self):
        self.conversions += 1
        return "PRIVATE_ARGUMENT_RECEIVING_MARKER"

    __str__ = __repr__


class NativeFailure(ValueError):
    def __init__(self):
        super().__init__("PRIVATE_EXCEPTION_RECEIVING_MARKER")
        self.conversions = 0

    def __str__(self):
        self.conversions += 1
        return super().__str__()


def application(threshold, enabled=True, silenced=False):
    handler = MemoryHandler()
    # configure() intentionally retains prior history; begin each control with
    # an empty buffer through the public configuration API.
    smonitor.configure(event_buffer_size=0)
    manager = smonitor.configure(
        level=threshold,
        enabled=enabled,
        handlers=[handler],
        silence=["argdigest.core.decorator"] if silenced else [],
        capture_warnings=False,
        capture_logging=False,
        capture_exceptions=False,
        args_summary=True,
        profiling=False,
        event_buffer_size=20,
        duplicate_policy="off",
    )
    return handler, manager


def assert_observation(handler, manager, expected, configuration, policy):
    assert [event["level"] for event in handler.events] == expected
    assert [event["level"] for event in manager.recent_events()] == expected
    assert manager.config is configuration
    assert smonitor.get_capture_policy() == policy


def assert_restricted(handler, value, failure):
    assert value.conversions == 0
    if isinstance(failure, NativeFailure):
        assert failure.conversions == 0
    payload = json.dumps(handler.events)
    assert "PRIVATE_ARGUMENT_RECEIVING_MARKER" not in payload
    assert "PRIVATE_EXCEPTION_RECEIVING_MARKER" not in payload


@pytest.mark.parametrize("catalog", [False, True], ids=["native", "catalog"])
@pytest.mark.parametrize("restricted", [False, True], ids=["detailed", "restricted"])
@pytest.mark.parametrize(
    "threshold,enabled,silenced,expected",
    [
        ("WARNING", True, False, ["ERROR"]),
        ("DEBUG", True, False, ["DEBUG"]),
        ("CRITICAL", True, False, []),
        ("WARNING", False, False, []),
        ("DEBUG", True, True, ["ERROR"]),
    ],
    ids=[
        "filtered-debug",
        "accepted-debug",
        "all-filtered",
        "disabled",
        "silenced-inner",
    ],
)
def test_body_failure_composition(
    catalog, restricted, threshold, enabled, silenced, expected
):
    handler, manager = application(threshold, enabled, silenced)
    configuration = manager.config
    value = PrivateValue()
    cause = LookupError("original cause")
    scope = smonitor.diagnostic_scope() if restricted else nullcontext()
    with scope:
        policy = smonitor.get_capture_policy()
        context = Context(function_name="body", argname="value", value=value)
        failure = DigestValueError(context=context) if catalog else NativeFailure()
        original_args = failure.args

        @arg_digest(config=DigestConfig(argument_digestion=False))
        def body(value):
            raise failure from cause

        @smonitor.signal(exception_level="ERROR")
        def outer(value):
            return body(value)

        # A second ERROR wrapper must not duplicate an admitted observation.
        operation = smonitor.signal(exception_level="ERROR")(outer)
        with warnings.catch_warnings(record=True) as recorded:
            warnings.simplefilter("always")
            with pytest.raises(type(failure)) as caught:
                operation(value)
        assert recorded == []
        assert caught.value is failure
        assert failure.args == original_args
        assert failure.__cause__ is cause
        assert_observation(handler, manager, expected, configuration, policy)
        if catalog:
            assert failure.context is context
            assert all(event["code"] == failure.code for event in handler.events)
        if restricted:
            assert_restricted(handler, value, failure)


@pytest.mark.parametrize("restricted", [False, True], ids=["detailed", "restricted"])
@pytest.mark.parametrize("stage", ["pipeline", "contract"])
@pytest.mark.parametrize("threshold", ["WARNING", "DEBUG"])
def test_failures_before_body_preserve_validation_and_diagnostics(
    restricted, stage, threshold
):
    handler, manager = application(threshold)
    configuration = manager.config
    value, failure = PrivateValue(), NativeFailure()
    cause = LookupError("original pipeline cause")
    failure.__cause__ = cause
    executed = []

    def reject(value, context):
        raise failure

    def body(value):
        executed.append(value)

    options = {"config": DigestConfig(argument_digestion=False)}
    if stage == "pipeline":
        options["map"] = {"value": {"kind": "receiving", "rules": [reject]}}
    target = arg_digest(**options)(body)
    operation = smonitor.signal(exception_level="ERROR")(target)
    scope = smonitor.diagnostic_scope() if restricted else nullcontext()
    with scope:
        policy = smonitor.get_capture_policy()
        with warnings.catch_warnings(record=True) as recorded:
            warnings.simplefilter("always")
            with pytest.raises(
                ValueError if stage == "pipeline" else TypeError
            ) as caught:
                operation(value, **({"typo": value} if stage == "contract" else {}))
        assert recorded == []
        assert executed == []
        if stage == "pipeline":
            assert caught.value is failure
            assert failure.args == ("PRIVATE_EXCEPTION_RECEIVING_MARKER",)
            assert failure.__cause__ is cause
            # Registry.run's ERROR signal admits the native exception first;
            # ArgDigest also emits its separate DEBUG pipeline diagnostic.
            expected = ["ERROR", "DEBUG"] if threshold == "DEBUG" else ["ERROR"]
            if threshold == "DEBUG":
                assert handler.events[-1]["code"] == "ARG-DBG-PIPELINE-001"
        else:
            expected = ["DEBUG" if threshold == "DEBUG" else "ERROR"]
            assert caught.value.code == "ARG-ERR-CONTRACT-001"
            assert all(event["code"] == caught.value.code for event in handler.events)
        assert_observation(handler, manager, expected, configuration, policy)
        if restricted:
            assert_restricted(handler, value, failure)
