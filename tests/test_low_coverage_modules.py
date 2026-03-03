from __future__ import annotations

import sys
import types
from contextlib import contextmanager

import numpy as np
import pytest

from argdigest import DigestTypeError, DigestValueError
from argdigest.contrib import pyunitwizard_support as puw_support
from argdigest.core import argument_loader
from argdigest.core.context import Context
from argdigest.core.errors_base import ArgDigestCatalogException, ArgDigestCatalogWarning
from argdigest.core.registry import Registry, get_pipelines
from argdigest.pipelines import data as data_pipelines


def _ctx(name: str = "x", profiling: bool = False) -> Context:
    return Context(function_name="f", argname=name, value=None, _profiling=profiling, audit_log=[])


def test_errors_base_default_extra_is_injected():
    exc = ArgDigestCatalogException(message="boom")
    warn = ArgDigestCatalogWarning(message="warn")
    assert isinstance(exc, Exception)
    assert isinstance(warn, Warning)


def test_registry_unregistered_kind_and_unknown_rule(monkeypatch):
    assert get_pipelines("kind_not_registered") == {}
    called = []
    monkeypatch.setattr("argdigest.core.registry.logger.warning", lambda msg: called.append(msg))

    out = Registry.run(kind="kind_not_registered", rules=["missing_rule", 42], value=1, ctx=_ctx("arg"))
    assert out == 1
    assert called and "Unknown rule type" in called[0]


def test_registry_profiled_callable_and_pydantic_like_rule():
    class FakeModel:
        @classmethod
        def model_validate(cls, value):
            return {"wrapped": value}

    def add_one(value, _ctx):
        return value + 1

    c = _ctx("feat", profiling=True)
    out = Registry.run(kind="none", rules=[add_one, FakeModel], value=1, ctx=c)
    assert out == {"wrapped": 2}
    assert len(c.audit_log) == 2
    assert c.audit_log[0]["rule"] == "add_one"
    assert c.audit_log[1]["rule"] == "Pydantic:FakeModel"


def test_argument_loader_error_branches(monkeypatch):
    with pytest.raises(ValueError, match="standardizer must be a callable or"):
        argument_loader.resolve_standardizer("invalid_path_without_attr")

    mod = types.ModuleType("tmp_std_module")
    mod.not_callable = 42
    sys.modules[mod.__name__] = mod
    try:
        with pytest.raises(TypeError, match="must resolve to a callable"):
            argument_loader.resolve_standardizer("tmp_std_module:not_callable")
    finally:
        sys.modules.pop(mod.__name__, None)

    with pytest.raises(TypeError, match="callable, a string, or None"):
        argument_loader.resolve_standardizer(123)

    with pytest.raises(ValueError, match="digestion_style must be"):
        argument_loader.load_argument_digesters("x", "bad-style")


def test_argument_loader_registry_and_package_guards():
    reg_mod = types.ModuleType("tmp_registry_mod")
    reg_mod.ARGUMENT_DIGESTERS = 7
    sys.modules[reg_mod.__name__] = reg_mod
    try:
        argument_loader._load_from_registry.cache_clear()
        with pytest.raises(TypeError, match="ARGUMENT_DIGESTERS must be a dict"):
            argument_loader._load_from_registry("tmp_registry_mod")
    finally:
        sys.modules.pop(reg_mod.__name__, None)
        argument_loader._load_from_registry.cache_clear()

    plain_mod = types.ModuleType("tmp_plain_mod")
    sys.modules[plain_mod.__name__] = plain_mod
    try:
        argument_loader._load_from_package.cache_clear()
        assert argument_loader._load_from_package("tmp_plain_mod") == {}
    finally:
        sys.modules.pop(plain_mod.__name__, None)
        argument_loader._load_from_package.cache_clear()


def test_data_pipelines_extra_branches(monkeypatch):
    arr = np.array([1, 2, 3])
    assert data_pipelines.to_numpy(arr, _ctx("arr")) is arr

    original_asarray = data_pipelines.np.asarray
    monkeypatch.setattr(data_pipelines.np, "asarray", lambda _v: (_ for _ in ()).throw(RuntimeError("x")))
    with pytest.raises(DigestTypeError, match="Cannot convert to numpy array"):
        data_pipelines.to_numpy("bad", _ctx("arr"))
    monkeypatch.setattr(data_pipelines.np, "asarray", original_asarray)

    if data_pipelines.HAS_PANDAS:
        import pandas as pd

        df = pd.DataFrame({"a": [1]})
        assert data_pipelines.to_dataframe(df, _ctx("df")) is df

        class FailingDataFrame:
            def __init__(self, _v):
                raise RuntimeError("x")

        monkeypatch.setattr(data_pipelines.pd, "DataFrame", FailingDataFrame)
        with pytest.raises(DigestTypeError, match="Cannot convert to pandas DataFrame"):
            data_pipelines.to_dataframe({"a": [1]}, _ctx("df"))

        with pytest.raises(DigestTypeError, match="Expected DataFrame"):
            data_pipelines.has_columns(["a"])([{"a": 1}], _ctx("df"))

    with pytest.raises(DigestValueError, match="Expected ndim=2"):
        data_pipelines.is_shape((2, 2))(np.array([1, 2]), _ctx("arr"))

    with pytest.raises(DigestTypeError, match="has no length"):
        data_pipelines.min_rows(2)(object(), _ctx("rows"))


def test_pyunitwizard_support_missing_dependency_context(monkeypatch):
    monkeypatch.setattr(puw_support, "HAS_PUW", False)
    with puw_support.context(form="pint", parser="pint"):
        pass
    with pytest.raises(DigestTypeError, match="pyunitwizard"):
        puw_support.is_quantity()(1.0, _ctx("q"))


def test_pyunitwizard_support_mapping_and_error_paths(monkeypatch):
    captured = {}

    @contextmanager
    def fake_context(**kwargs):
        captured.update(kwargs)
        yield

    class FakePuw:
        context = staticmethod(fake_context)

        @staticmethod
        def standardize(_value):
            raise RuntimeError("boom")

        @staticmethod
        def is_quantity(_value):
            return False

    monkeypatch.setattr(puw_support, "HAS_PUW", True)
    monkeypatch.setattr(puw_support, "puw", FakePuw)

    with puw_support.context(form="x", parser="y", standard_units=["nm"]):
        pass
    assert captured["default_form"] == "x"
    assert captured["default_parser"] == "y"
    assert captured["standard_units"] == ["nm"]

    with pytest.raises(DigestValueError, match="Standardization failed"):
        puw_support.standardize()("value", _ctx("q"))

    with pytest.raises(DigestTypeError, match="Expected a quantity"):
        puw_support.is_quantity()("not_quantity", _ctx("q"))
