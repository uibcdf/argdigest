import pytest

from argdigest import (
    argument_digest,
    digest,
    register_pipeline,
    DigestNotDigestedError,
    DigestNotDigestedWarning,
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

    @arg_digest(digestion_style="decorator", standardizer=standardizer, strictness="ignore")
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