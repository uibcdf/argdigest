from __future__ import annotations

import warnings

import pytest

from argdigest import arg_digest
from argdigest.core.decorator import get_digester_metadata
from argdigest.core.errors import DigestNotDigestedError


def test_get_digester_metadata_ambiguous_value_param_raises():
    def digest_a(x, y, caller=None):
        return x

    with pytest.raises(DigestNotDigestedError, match="Cannot determine value parameter"):
        get_digester_metadata(digest_a, "a")


def test_type_check_missing_beartype_falls_back_to_runtime_warning(monkeypatch):
    original_import = __import__

    def _import(name, *args, **kwargs):
        if name == "beartype":
            raise ImportError("no beartype")
        if name.startswith("smonitor"):
            raise ImportError("no smonitor integration")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", _import)

    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        @arg_digest(digestion_style="auto", strictness="ignore", type_check=True)
        def f(a):
            return a

        assert f(3) == 3
        assert any("type_check=True but 'beartype' is not installed" in str(w.message) for w in rec)


def test_var_keyword_flattening_and_digestion_params_injection():
    from argdigest import argument_digest

    @argument_digest("a")
    def digest_a(a, factor, caller=None):
        return int(a) * factor

    @arg_digest(digestion_style="decorator", strictness="ignore", factor=10)
    def h(a, **kwargs):
        return a, kwargs

    out_a, out_kwargs = h("3", extra=7)
    assert out_a == 30
    # **kwargs were flattened into bound args; function receives kwargs as usual.
    assert out_kwargs == {"extra": 7}


def test_pipeline_target_missing_argument_is_skipped():
    @arg_digest(
        digestion_style="auto",
        strictness="ignore",
        map={"missing_arg": {"kind": "data", "rules": ["to_numpy"]}},
    )
    def f(a):
        return a

    assert f(5) == 5
