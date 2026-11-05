"""Invalid consumer registrations retain rejection and name their owner (#50)."""

import sys
from contextlib import nullcontext
from types import ModuleType

import pytest
import smonitor
from smonitor.handlers.memory import MemoryHandler

from argdigest import DigestConfig, DigestNotDigestedError, arg_digest


class Opaque:
    def __init__(self):
        self.conversions = 0

    def __repr__(self):
        self.conversions += 1
        return "PRIVATE_DIGESTER_DEFAULT"

    __str__ = __repr__


@pytest.fixture
def observations():
    manager = smonitor.get_manager()
    previous, handlers = manager.config, list(manager._handlers)
    handler = MemoryHandler()
    smonitor.configure(
        level="DEBUG",
        enabled=True,
        handlers=[handler],
        capture_warnings=False,
        capture_logging=False,
    )
    yield handler
    smonitor.configure(
        level=previous.level,
        profile=previous.profile,
        enabled=previous.enabled,
        handlers=handlers,
        capture_warnings=previous.capture_warnings,
        capture_logging=previous.capture_logging,
    )


def registered(monkeypatch, digester, name):
    module = ModuleType(name)
    module.ARGUMENT_DIGESTERS = {"atom_names": digester}
    monkeypatch.setitem(sys.modules, name, module)
    return DigestConfig(
        digestion_source=name, digestion_style="registry", strictness="error"
    )


@pytest.mark.parametrize("restricted", [False, True])
@pytest.mark.parametrize("profile", ["user", "dev", "qa"])
def test_ambiguous_registration_names_consumer_without_formatting_defaults(
    monkeypatch, observations, restricted, profile, request
):
    if restricted and not hasattr(smonitor, "diagnostic_scope"):
        if request.config.getoption("--require-scoped-capture"):
            pytest.fail("Installed qualification requires scoped capture")
        pytest.skip("Historical provider lacks scoped capture")
    smonitor.configure(profile=profile)
    default, value = Opaque(), Opaque()

    def ambiguous(value, caller=None, native_constructor=default):
        pytest.fail("Invalid digester must not execute")

    config = registered(monkeypatch, ambiguous, f"consumer_50_{profile}_{restricted}")

    @arg_digest(config=config)
    def consumer(atom_names):
        pytest.fail("Invalid registration must not reach the consumer body")

    scope = smonitor.diagnostic_scope() if restricted else nullcontext()
    with scope, pytest.raises(DigestNotDigestedError) as caught:
        consumer(value)
    error = caught.value
    assert type(error) is DigestNotDigestedError
    assert error.code == "ARG-ERR-DIGESTER-001"
    assert error.context.argname == "atom_names"
    assert error.context.function_name.endswith(".consumer")
    assert error.context.value is None
    assert default.conversions == 0
    text = str(error)
    assert "ArgDigest problem rather than yours" not in text
    assert "report it" not in text.lower()
    assert "PRIVATE_DIGESTER_DEFAULT" not in text
    assert any(event.get("code") == error.code for event in observations.events)
    if restricted:
        assert value.conversions == 0
        assert "parameters" not in error.extra
        assert "digester" not in error.extra
    else:
        assert "ambiguous" in text
        assert "atom_names" in text
        assert "consumer" in text
        assert "value, caller, native_constructor" in text
        assert "Name the value parameter" in text


def test_bad_registration_context_is_not_cached_across_consumers(monkeypatch):
    def ambiguous(value, dependency=None):
        return value

    config = registered(monkeypatch, ambiguous, "consumer_50_shared")

    def first(atom_names):
        return atom_names

    def second(atom_names):
        return atom_names

    for function in (first, second):
        with pytest.raises(DigestNotDigestedError) as caught:
            arg_digest(config=config)(function)(["C1"])
        assert caught.value.context.function_name.endswith("." + function.__name__)


def test_naming_the_value_parameter_repairs_registration(monkeypatch):
    default = Opaque()

    def corrected(atom_names, caller=None, native_constructor=default):
        return atom_names

    config = registered(monkeypatch, corrected, "consumer_50_corrected")

    @arg_digest(config=config)
    def consumer(atom_names):
        return atom_names

    value = ["C1"]
    assert consumer(value) is value
    assert default.conversions == 0


@pytest.mark.parametrize("exact_name", [False, True])
def test_valid_callable_never_reads_diagnostic_labels(monkeypatch, exact_name):
    reads = []

    class Labels(type):
        def __getattribute__(cls, name):
            if name in {"__module__", "__qualname__"}:
                reads.append(name)
                raise RuntimeError("diagnostic labels are unavailable")
            return super().__getattribute__(name)

    class Exact(metaclass=Labels):
        def __call__(self, atom_names):
            return atom_names

    class SoleValue(metaclass=Labels):
        def __call__(self, value):
            return value

    config = registered(
        monkeypatch,
        Exact() if exact_name else SoleValue(),
        f"consumer_53_valid_{exact_name}",
    )

    @arg_digest(config=config)
    def consumer(atom_names):
        return atom_names

    value = ["C1"]
    assert consumer(value) is value
    assert reads == []


@pytest.mark.parametrize("restricted", [False, True])
@pytest.mark.parametrize("label_mode", ["raises", "opaque"])
def test_unavailable_label_keeps_configuration_error(
    monkeypatch, restricted, label_mode, request
):
    if restricted and not hasattr(smonitor, "diagnostic_scope"):
        if request.config.getoption("--require-scoped-capture"):
            pytest.fail("Installed qualification requires scoped capture")
        pytest.skip("Historical provider lacks scoped capture")
    reads = []
    label = Opaque()

    class Labels(type):
        def __getattribute__(cls, name):
            if name in {"__module__", "__qualname__"}:
                reads.append(name)
                if label_mode == "raises":
                    raise RuntimeError("diagnostic labels are unavailable")
                return label
            return super().__getattribute__(name)

    class Ambiguous(metaclass=Labels):
        def __call__(self, value, dependency=None):
            pytest.fail("ambiguous digester must not execute")

    config = registered(
        monkeypatch, Ambiguous(), f"consumer_53_bad_{restricted}_{label_mode}"
    )

    @arg_digest(config=config)
    def consumer(atom_names):
        pytest.fail("consumer body must not execute")

    scope = smonitor.diagnostic_scope() if restricted else nullcontext()
    with scope, pytest.raises(DigestNotDigestedError) as caught:
        consumer(["C1"])
    assert caught.value.code == "ARG-ERR-DIGESTER-001"
    assert caught.value.context.argname == "atom_names"
    assert caught.value.context.function_name.endswith(".consumer")
    assert label.conversions == 0
    if restricted:
        assert reads == []
    else:
        assert caught.value.extra["digester"] == "configured digester"
