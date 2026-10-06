"""ArgDigest must prevent diagnostic conversion before SMonitor emission."""

import asyncio
import json
import traceback
import warnings
from concurrent.futures import ThreadPoolExecutor

import pytest
import smonitor
from smonitor.handlers.memory import MemoryHandler

from argdigest import (
    DigestConfig,
    DigestError,
    DigestValueError,
    UnknownArgumentError,
    arg_digest,
    argument_digest,
)
from argdigest.core.diagnostics import get_capture_policy
from argdigest.core.registry import Registry


class Opaque:
    def __init__(self):
        self.repr_calls = self.str_calls = 0

    def __repr__(self):
        self.repr_calls += 1
        return "OPAQUE_CAPTURE_MARKER"

    def __str__(self):
        self.str_calls += 1
        return "OPAQUE_CAPTURE_MARKER"

    def __gt__(self, other):
        return False


class NativeError(ValueError):
    def __init__(self):
        super().__init__("NATIVE_CAPTURE_MARKER")
        self.str_calls = 0

    def __str__(self):
        self.str_calls += 1
        return "NATIVE_CAPTURE_MARKER"


@pytest.fixture
def capture_api():
    if not hasattr(smonitor, "diagnostic_scope"):
        pytest.skip("Scoped capture is not available in this SMonitor version")
    handler = MemoryHandler()
    manager = smonitor.get_manager()
    previous = manager.config
    previous_handlers = list(manager._handlers)
    smonitor.configure(
        handlers=[handler],
        level="DEBUG",
        enabled=True,
        args_summary=True,
        capture_logging=False,
        capture_warnings=False,
    )
    yield handler
    smonitor.configure(
        handlers=previous_handlers,
        level=previous.level,
        enabled=previous.enabled,
        args_summary=previous.args_summary,
        capture_logging=previous.capture_logging,
        capture_warnings=previous.capture_warnings,
        profiling=previous.profiling,
    )


def assert_no_payload(handler):
    serialized = json.dumps(handler.events)
    assert "OPAQUE_CAPTURE_MARKER" not in serialized
    assert "NATIVE_CAPTURE_MARKER" not in serialized
    for event in handler.events:
        extra = event.get("extra", {})
        assert "cause_message" not in extra
        assert "all_args" not in extra
        assert "value" not in extra


@pytest.mark.parametrize("stage", ["digestion", "pipeline"])
@pytest.mark.parametrize("selection", ["decorator", "config", "ambient"])
def test_failures_never_convert_values_or_native_errors(capture_api, stage, selection):
    value, native = Opaque(), NativeError()
    cause = LookupError("original cause")
    native.__cause__ = cause

    def reject(value, ctx=None):
        raise native

    kwargs = {}
    if stage == "digestion":
        argument_digest("value")(reject)
        kwargs.update(digestion_style="decorator", strictness="error")
    else:
        kwargs["map"] = {"value": {"kind": "capture-test", "rules": [reject]}}
    if selection == "decorator":
        kwargs["capture_policy"] = "metadata_only"
    elif selection == "config":
        kwargs["config"] = DigestConfig(
            capture_policy="metadata_only", strictness="ignore"
        )
    target = arg_digest(**kwargs)(lambda value: value)
    with (
        smonitor.diagnostic_scope()
        if selection == "ambient"
        else smonitor.diagnostic_scope(smonitor.CapturePolicy())
    ):
        with pytest.raises(NativeError) as caught:
            target(value)
    assert caught.value is native
    assert native.__cause__ is cause
    assert "reject" in [
        frame.name for frame in traceback.extract_tb(native.__traceback__)
    ]
    assert value.repr_calls == value.str_calls == native.str_calls == 0
    code = "ARG-DBG-DIGEST-001" if stage == "digestion" else "ARG-DBG-PIPELINE-001"
    events = [event for event in capture_api.events if event.get("code") == code]
    assert events and events[-1]["message"]
    assert events[-1]["extra"]["argname"] == "value"
    assert_no_payload(capture_api)


def test_callable_rules_and_profiling_do_not_stringify_rules(capture_api):
    class Rule(Opaque):
        def __call__(self, value, ctx):
            assert ctx.value is value
            assert ctx.all_args["value"] is value
            return "normalized"

    rule, value = Rule(), Opaque()

    @arg_digest.map(
        capture_policy="metadata_only",
        profiling=True,
        value={"kind": "capture", "rules": [rule]},
    )
    def target(value):
        return value

    assert target(value) == "normalized"
    assert target.audit_log[0]["duration"] >= 0
    assert rule.repr_calls == rule.str_calls == value.repr_calls == value.str_calls == 0
    assert_no_payload(capture_api)


@pytest.mark.parametrize("fault", ["function", "value", "normalization"])
def test_contracts_remain_active_and_catalog_diagnostics_are_safe(capture_api, fault):
    value = Opaque()
    if fault == "function":

        @arg_digest(capture_policy="metadata_only")
        def target(value):
            pytest.fail("body must not execute")

        with pytest.raises(UnknownArgumentError):
            target(value, typo=value)
    elif fault == "value":

        @arg_digest.map(
            capture_policy="metadata_only",
            value={"kind": "std", "rules": ["is_positive"]},
        )
        def target(value):
            pytest.fail("body must not execute")

        with pytest.raises(DigestValueError) as caught:
            target(value)
        assert caught.value.context.value is value
        assert "detail" not in caught.value.extra
    else:
        from tests.mock_axis_one import api

        with smonitor.diagnostic_scope():
            with pytest.raises(DigestError):
                api.get("s", coords=value, coordinates=value)
    assert value.repr_calls == value.str_calls == 0
    assert_no_payload(capture_api)
    assert any(event.get("code", "").startswith("ARG-") for event in capture_api.events)


def test_detailed_option_cannot_relax_ambient_restrictions(capture_api):
    native = NativeError()

    @arg_digest(capture_policy="detailed")
    def target(value):
        raise native

    with smonitor.diagnostic_scope():
        with pytest.raises(NativeError):
            target(Opaque())
    assert native.str_calls == 0
    assert get_capture_policy() == smonitor.CapturePolicy()
    assert_no_payload(capture_api)


def test_fallback_failure_preserves_native_exception(capture_api, monkeypatch):
    native, diagnostic = NativeError(), NativeError()

    def broken_emit(*args, **kwargs):
        raise diagnostic

    monkeypatch.setattr(smonitor, "emit", broken_emit)

    def reject(value, ctx):
        raise native

    @arg_digest.map(
        capture_policy="metadata_only", value={"kind": "capture", "rules": [reject]}
    )
    def target(value):
        return value

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        with pytest.raises(NativeError) as caught:
            target(Opaque())
    assert caught.value is native
    assert native.str_calls == diagnostic.str_calls == 0


def test_rich_defaults_keep_native_text_and_pipeline_execution(capture_api):
    native = NativeError()

    def reject(value, ctx):
        raise native

    @arg_digest.map(value={"kind": "capture", "rules": [reject]})
    def target(value):
        return value

    with pytest.raises(NativeError) as caught:
        target("plain")
    assert caught.value is native
    assert native.str_calls > 0
    assert "NATIVE_CAPTURE_MARKER" in json.dumps(capture_api.events)


def test_threads_keep_per_decorator_policy_independent(capture_api):
    def run(policy):
        value, native = Opaque(), NativeError()

        def reject(value, ctx):
            raise native

        target = arg_digest(
            capture_policy=policy, map={"value": {"kind": "capture", "rules": [reject]}}
        )(lambda value: value)
        with pytest.raises(NativeError):
            target(value)
        assert get_capture_policy() == smonitor.CapturePolicy()
        return native.str_calls

    with ThreadPoolExecutor(max_workers=2) as pool:
        restricted, detailed = list(pool.map(run, ["metadata_only", "detailed"]))
    assert restricted == 0 and detailed > 0


def test_interleaved_tasks_inherit_scopes_without_global_reconfiguration(capture_api):
    async def run(policy):
        native = NativeError()

        @arg_digest()
        def target(value):
            raise native

        with smonitor.diagnostic_scope(policy):
            await asyncio.sleep(0)
            with pytest.raises(NativeError):
                target(Opaque())
        return native.str_calls

    async def collect():
        return await asyncio.gather(
            run(smonitor.METADATA_ONLY), run(smonitor.CapturePolicy())
        )

    restricted, detailed = asyncio.run(collect())
    assert restricted == 0 and detailed > 0


def test_old_provider_keeps_defaults_but_rejects_requested_restriction(monkeypatch):
    monkeypatch.delattr(smonitor, "CapturePolicy", raising=False)

    @arg_digest.map(value={"kind": "std", "rules": ["strip"]})
    def target(value):
        return value

    assert target(" value ") == "value"
    with pytest.raises(DigestError) as caught:
        arg_digest(capture_policy="metadata_only")(lambda value: value)
    assert caught.value.code == "ARG-ERR-CAPTURE-001"


@pytest.mark.parametrize("config_type", ["json", "yaml", "py"])
def test_capture_policy_loads_from_files(tmp_path, config_type):
    from argdigest.config import load_from_file

    path = tmp_path / ("config." + config_type)
    path.write_text(
        {
            "json": '{"capture_policy": "metadata_only"}',
            "yaml": "capture_policy: metadata_only",
            "py": 'CAPTURE_POLICY = "metadata_only"',
        }[config_type]
    )
    assert load_from_file(path).capture_policy == "metadata_only"


@pytest.mark.parametrize(
    "adapter",
    ["convert", "standardize", "canonical", "model", "model-helper", "numpy", "pandas"],
)
def test_adapter_errors_do_not_stringify_native_failures(
    capture_api, monkeypatch, adapter
):
    from argdigest.contrib import pyunitwizard_support as support
    from argdigest.contrib.pydantic_support import pydantic_pipeline
    from argdigest.core.context import Context
    from argdigest.pipelines import data

    native, value = NativeError(), Opaque()
    ctx = Context(function_name="consumer", argname="value", value=value)

    def fail(*args, **kwargs):
        raise native

    class Provider:
        convert = standardize = fail
        fast_track = type("FastTrack", (), {"to_nanometers": staticmethod(fail)})

    class Model:
        model_validate = staticmethod(fail)

    if adapter in ("convert", "standardize", "canonical"):
        monkeypatch.setattr(support, "HAS_PUW", True)
        monkeypatch.setattr(support, "puw", Provider)
        operation = {
            "convert": lambda: support.convert("nm")(value, ctx),
            "standardize": lambda: support.standardize()(value, ctx),
            "canonical": lambda: support.nm_float64()(value, ctx),
        }[adapter]
    elif adapter == "model":

        def operation():
            return Registry.run("capture", [Model], value, ctx)
    elif adapter == "model-helper":

        def operation():
            return pydantic_pipeline(Model)(value, ctx)
    elif adapter == "numpy":

        class Numpy:
            ndarray = tuple
            asarray = staticmethod(fail)

        monkeypatch.setattr(data, "np", Numpy)

        def operation():
            return data.to_numpy(value, ctx)
    else:

        class Pandas:
            DataFrame = staticmethod(fail)

        # isinstance needs a class; constructor failure occurs only after that check.
        class DataFrame:
            def __new__(cls, *args):
                raise native

        Pandas.DataFrame = DataFrame
        monkeypatch.setattr(data, "pd", Pandas)

        def operation():
            return data.to_dataframe(value, ctx)

    with smonitor.diagnostic_scope():
        with pytest.raises((DigestError, ValueError)) as caught:
            operation()
    assert caught.value.__cause__ is native
    assert native.str_calls == value.str_calls == value.repr_calls == 0
    assert_no_payload(capture_api)


def test_type_check_fallback_obeys_policy_before_construction(capture_api, monkeypatch):
    import builtins

    original_import = builtins.__import__

    def refuse(name, *args, **kwargs):
        if name == "beartype" or name.startswith("smonitor"):
            raise ImportError("FICTITIOUS_IMPORT_MARKER")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", refuse)
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")

        @arg_digest(type_check=True, capture_policy="metadata_only")
        def target(value):
            return value

        value = Opaque()
        assert target(value) is value
    assert recorded
    assert all("FICTITIOUS_IMPORT_MARKER" not in str(item.message) for item in recorded)
    assert value.str_calls == value.repr_calls == 0


def test_custom_provider_policy_is_preserved_in_plan(capture_api):
    policy = smonitor.CapturePolicy(arguments=False, exception_text=False)
    target = arg_digest(capture_policy=policy)(lambda value: value)
    assert target.digestion_plan.capture_policy == policy
    assert target(Opaque()).str_calls == 0


def test_restricted_config_with_pipeline_only_keeps_value_validation(capture_api):
    value = Opaque()
    cfg = DigestConfig(
        capture_policy="metadata_only", argument_digestion=False, strictness="error"
    )
    target = arg_digest.map(
        config=cfg, value={"kind": "std", "rules": ["is_positive"]}
    )(lambda value: value)
    with pytest.raises(DigestValueError) as caught:
        target(value)
    assert caught.value.context.value is value
    assert value.str_calls == value.repr_calls == 0
    assert_no_payload(capture_api)


def test_invalid_policy_is_refused_without_stringification(capture_api):
    value = Opaque()
    with pytest.raises(DigestValueError):
        arg_digest(capture_policy=value)(lambda value: value)
    assert value.str_calls == value.repr_calls == 0


@pytest.mark.parametrize(
    "factory",
    ["has_ndim", "is_shape", "is_dtype", "has_columns", "min_rows", "convert"],
)
def test_factory_labels_never_format_parameters_in_active_scope(capture_api, factory):
    from argdigest.contrib import pyunitwizard_support as support
    from argdigest.pipelines import data

    value = Opaque()
    parameter = {"is_shape": (value,), "has_columns": [value]}.get(factory, value)
    owner = support if factory == "convert" else data
    with smonitor.diagnostic_scope():
        pipeline = getattr(owner, factory)(parameter)
    assert pipeline.__name__ == ("puw.convert" if factory == "convert" else factory)
    assert value.str_calls == value.repr_calls == 0
    assert_no_payload(capture_api)


@pytest.mark.parametrize("factory", ["has_ndim", "is_shape", "has_columns"])
def test_parameterized_validation_details_never_format_parameters(
    capture_api, monkeypatch, factory
):
    from argdigest.core.context import Context
    from argdigest.pipelines import data

    parameter = Opaque()
    if factory == "has_columns":

        class Frame:
            columns = []

        class Pandas:
            DataFrame = Frame

        monkeypatch.setattr(data, "pd", Pandas)
        value, parameters = Frame(), [parameter]
    else:
        import numpy as np

        value = np.zeros(1)
        parameters = (parameter,) if factory == "is_shape" else parameter
    ctx = Context(function_name="consumer", argname="value", value=value)
    with smonitor.diagnostic_scope():
        pipeline = getattr(data, factory)(parameters)
        with pytest.raises(DigestValueError):
            pipeline(value, ctx)
    assert parameter.str_calls == parameter.repr_calls == 0
    assert_no_payload(capture_api)


def test_standardizer_signature_error_never_formats_default_values(capture_api):
    value = Opaque()

    def incompatible(caller=value):
        return {}

    with pytest.raises(TypeError, match="must be callable"):
        arg_digest(capture_policy="metadata_only", standardizer=incompatible)(
            lambda value: value
        )
    assert value.str_calls == value.repr_calls == 0
    assert_no_payload(capture_api)


def test_model_helper_never_formats_model_metaclass(capture_api):
    from argdigest.contrib.pydantic_support import model_from_dict

    formatted = []

    class Meta(type):
        def __repr__(cls):
            formatted.append(cls)
            return "OPAQUE_CAPTURE_MARKER"

    class Model(metaclass=Meta):
        pass

    with smonitor.diagnostic_scope():
        with pytest.raises(TypeError):
            model_from_dict(Model, Opaque())
    assert formatted == []
    assert_no_payload(capture_api)


def test_bounded_metadata_fallback_preserves_native_failure(capture_api):
    native, value = NativeError(), Opaque()

    def reject(value, ctx):
        raise native

    target = arg_digest.map(value={"kind": "capture", "rules": [reject]})(
        lambda value: value
    )
    facts = {f"approved_{index}": index for index in range(32)}
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        with smonitor.diagnostic_scope(safe_extra=facts):
            with pytest.raises(NativeError) as caught:
                target(value)
    assert caught.value is native
    assert recorded and all(
        "NATIVE_CAPTURE_MARKER" not in str(w.message) for w in recorded
    )
    assert native.str_calls == value.str_calls == value.repr_calls == 0
    assert_no_payload(capture_api)
