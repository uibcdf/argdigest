from __future__ import annotations

import inspect

import pytest

import argdigest
from argdigest import DigestConfig, arg_digest
from argdigest.core.config import get_defaults, set_defaults


EXPECTED_PUBLIC_API = [
    "arg_digest",
    "register_pipeline",
    "get_pipelines",
    "argument_digest",
    "DigestConfig",
    "pipelines",
    "DigestError",
    "DigestTypeError",
    "DigestValueError",
    "DigestInvariantError",
    "DigestNotDigestedError",
    "DigestNotDigestedWarning",
]


def test_public_api_surface_is_stable():
    assert argdigest.__all__ == EXPECTED_PUBLIC_API
    for name in EXPECTED_PUBLIC_API:
        assert hasattr(argdigest, name)


def test_public_callable_signatures():
    sig = inspect.signature(argdigest.arg_digest)
    assert "kind" in sig.parameters
    assert "rules" in sig.parameters
    assert "map" in sig.parameters
    assert "digestion_source" in sig.parameters
    assert "digestion_style" in sig.parameters
    assert "strictness" in sig.parameters
    assert "config" in sig.parameters
    assert "type_check" in sig.parameters
    assert "puw_context" in sig.parameters
    assert "profiling" in sig.parameters
    assert "digestion_params" in sig.parameters
    assert sig.parameters["kind"].kind is inspect.Parameter.KEYWORD_ONLY
    assert sig.parameters["digestion_params"].kind is inspect.Parameter.VAR_KEYWORD

    sig_map = inspect.signature(argdigest.arg_digest.map)
    assert "type_check" in sig_map.parameters
    assert "puw_context" in sig_map.parameters
    assert "profiling" in sig_map.parameters
    assert "config" in sig_map.parameters
    assert "map_config" in sig_map.parameters
    assert sig_map.parameters["map_config"].kind is inspect.Parameter.VAR_KEYWORD

    assert list(inspect.signature(argdigest.argument_digest).parameters) == ["name"]
    assert list(inspect.signature(argdigest.register_pipeline).parameters) == ["kind", "name"]
    assert list(inspect.signature(argdigest.get_pipelines).parameters) == ["kind"]


def test_decorator_explicit_strictness_overrides_defaults():
    original = get_defaults()
    try:
        set_defaults(DigestConfig(digestion_style="decorator", strictness="error"))

        @arg_digest(digestion_style="decorator", strictness="ignore")
        def f(a):
            return a

        # If defaults took precedence, this would raise DigestNotDigestedError.
        assert f("x") == "x"
    finally:
        set_defaults(original)


def test_config_object_controls_runtime_when_not_overridden():
    cfg = DigestConfig(digestion_style="decorator", strictness="error")

    @arg_digest(config=cfg)
    def f(a):
        return a

    with pytest.raises(argdigest.DigestNotDigestedError):
        f("x")
