import gc
import weakref

import pytest

from argdigest import (
    DigestNotDigestedError,
    DigestNotDigestedWarning,
    arg_digest,
    argument_digest,
    register_pipeline,
)
from argdigest.core.config import DigestConfig, set_defaults


def test_argument_digest_basic():
    @argument_digest("a")
    def digest_a(a, caller=None):
        return int(a)

    @arg_digest(digestion_style="decorator", strictness="ignore")
    def f(a, b):
        return a, b

    a, b = f("5", "x")
    assert a == 5
    assert b == "x"


def test_argument_dependency_resolution():
    @argument_digest("a")
    def digest_a_local(a, caller=None):
        return int(a) * 2

    @argument_digest("b")
    def digest_b(b, a, caller=None):
        return int(b) + a

    @arg_digest(digestion_style="decorator", strictness="ignore")
    def f(a, b):
        return a, b

    a, b = f("2", "1")
    assert a == 4
    assert b == 5


def test_standardizer_hook():
    def standardizer(caller, kwargs):
        if "name" in kwargs:
            kwargs = dict(kwargs)
            kwargs["element_name"] = kwargs.pop("name")
        return kwargs

    @arg_digest(
        digestion_style="decorator", standardizer=standardizer, strictness="ignore"
    )
    def f(**kwargs):
        return kwargs

    out = f(name="alpha")
    assert "element_name" in out
    assert out["element_name"] == "alpha"


def test_skip_digestion_bypasses_argument_digesters():
    @arg_digest(digestion_style="decorator", strictness="ignore")
    def f(a, skip_digestion=False):
        return a

    assert f("5", skip_digestion=True) == "5"


def test_only_literal_true_skips_digestion_before_validating_the_flag():
    seen = []

    @argument_digest("value")
    def digest_value(value):
        seen.append("value")
        return int(value)

    @argument_digest("skip_digestion")
    def digest_skip_digestion(skip_digestion):
        seen.append("skip_digestion")
        if type(skip_digestion) is not bool:
            raise TypeError("skip_digestion must be a bool")
        return skip_digestion

    @arg_digest(digestion_style="decorator", strictness="error")
    def f(value, skip_digestion=False):
        return value

    assert f("5", skip_digestion=True) == "5"
    assert f("5", True) == "5"
    assert seen == []

    assert f("5", skip_digestion=False) == 5
    assert "value" in seen
    assert "skip_digestion" in seen

    for bad_value in ("yes", "False", 1):
        with pytest.raises(TypeError, match="skip_digestion must be a bool"):
            f("5", skip_digestion=bad_value)
        with pytest.raises(TypeError, match="skip_digestion must be a bool"):
            f("5", bad_value)


def test_classmethod_receiver_is_not_digested_in_either_decorator_order():
    @argument_digest("value")
    def digest_value(value):
        return int(value)

    class Example:
        @classmethod
        @arg_digest(digestion_style="decorator", strictness="error")
        def inner(cls, value):
            return cls, value

        @arg_digest(digestion_style="decorator", strictness="error")
        @classmethod
        def outer(cls, value):
            return cls, value

    assert Example.inner("5") == (Example, 5)
    assert Example.outer("6") == (Example, 6)


def test_free_function_cls_parameter_is_still_digested():
    @argument_digest("cls")
    def digest_cls(cls):
        return int(cls)

    @arg_digest(digestion_style="decorator", strictness="error")
    def f(cls):
        return cls

    assert f("7") == 7


def test_strictness_error_for_undigested():
    @arg_digest(digestion_style="decorator", strictness="error")
    def f(a, b):
        return a, b

    with pytest.raises(DigestNotDigestedError):
        f("5", "x")


def test_strictness_warn_for_undigested():
    @arg_digest(digestion_style="decorator", strictness="warn")
    def f(a, b):
        return a, b

    with pytest.warns(DigestNotDigestedWarning):
        f("5", "x")


def test_dual_mode_argument_then_pipeline():
    @register_pipeline(kind="x", name="double")
    def double(value, ctx):
        return value * 2

    @argument_digest("a")
    def digest_a(a, caller=None):
        return int(a)

    @arg_digest(
        digestion_style="decorator",
        strictness="ignore",
        map={"a": {"kind": "x", "rules": ["double"]}},
    )
    def f(a):
        return a

    assert f("5") == 10


def test_config_module_defaults():
    @argument_digest("a")
    def digest_a(a, caller=None):
        return int(a)

    cfg = DigestConfig(digestion_style="decorator", strictness="ignore")
    set_defaults(cfg)

    @arg_digest()
    def f(a):
        return a

    assert f("7") == 7


def test_cyclic_dependency_error_message():
    """Test that cyclic dependencies raise an error with the full cycle path."""

    @argument_digest("x_cyc")
    def digest_x(x_cyc, y_cyc, caller=None):
        return x_cyc

    @argument_digest("y_cyc")
    def digest_y(y_cyc, x_cyc, caller=None):
        return y_cyc

    @arg_digest(digestion_style="decorator")
    def f(x_cyc, y_cyc):
        return x_cyc, y_cyc

    with pytest.raises(DigestNotDigestedError) as excinfo:
        f(1, 2)

    msg = str(excinfo.value)
    # The order depends on iteration, but it should contain one of these paths
    assert "x_cyc -> y_cyc -> x_cyc" in msg or "y_cyc -> x_cyc -> y_cyc" in msg


def test_argument_digestion_does_not_retain_arguments_in_a_reference_cycle():
    class Payload:
        pass

    @arg_digest(digestion_style="decorator", strictness="ignore")
    def consume(cycle_probe_payload):
        return None

    payload = Payload()
    payload_reference = weakref.ref(payload)
    gc.collect()
    garbage_collection_was_enabled = gc.isenabled()
    gc.disable()
    try:
        consume(payload)
        del payload
        assert payload_reference() is None
    finally:
        if garbage_collection_was_enabled:
            gc.enable()
        gc.collect()
