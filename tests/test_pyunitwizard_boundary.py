"""The optional adapter imports its provider only when an operation needs it."""

import subprocess
import sys

import pytest

from argdigest import DigestTypeError
from argdigest.contrib import pyunitwizard_support as support
from argdigest.core.context import Context


def test_adapter_import_and_factory_creation_do_not_import_pyunitwizard():
    script = """
import builtins
import sys

original_import = builtins.__import__
def refuse_provider(name, *args, **kwargs):
    if name == 'pyunitwizard' or name.startswith('pyunitwizard.'):
        raise AssertionError('adapter imported the optional provider before use')
    return original_import(name, *args, **kwargs)

builtins.__import__ = refuse_provider
from argdigest.contrib import pyunitwizard_support as support
support.check(unit='nm')
support.standardize()
support.convert('nm')
support.is_quantity()
support.nm_float64(ndim=1)
assert not any(name == 'pyunitwizard' or name.startswith('pyunitwizard.')
               for name in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_missing_provider_keeps_argument_context_and_catalog_diagnostic(monkeypatch):
    monkeypatch.setattr(support, "HAS_PUW", False)
    monkeypatch.setattr(support, "puw", None)
    ctx = Context(
        function_name="set_distance", argname="distance", value=1, all_args={}
    )

    with pytest.raises(DigestTypeError) as error:
        support.convert("nm")(1, ctx)

    assert error.value.code == "ARG-ERR-OPTDEP-001"
    assert error.value.context is ctx
    assert "install_optional:argdigest[pyunitwizard]" in error.value.hint


def test_provider_load_is_deferred_until_execution_and_reused(monkeypatch):
    class Provider:
        @staticmethod
        def is_quantity(value):
            return value == "quantity"

    calls = []

    def load():
        calls.append("load")
        return Provider

    monkeypatch.setattr(support, "HAS_PUW", True)
    monkeypatch.setattr(support, "puw", None)
    monkeypatch.setattr(support, "_load_puw", load)
    pipeline = support.is_quantity()
    assert calls == []
    assert pipeline("quantity", None) == "quantity"
    assert pipeline("quantity", None) == "quantity"
    assert calls == ["load"]


def test_transitive_import_failure_is_preserved(monkeypatch):
    import builtins

    failure = ModuleNotFoundError("missing provider backend", name="provider_backend")
    original_import = builtins.__import__

    def broken_provider(name, *args, **kwargs):
        if name == "pyunitwizard":
            raise failure
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(support, "HAS_PUW", True)
    monkeypatch.setattr(support, "puw", None)
    monkeypatch.setattr(builtins, "__import__", broken_provider)

    with pytest.raises(ModuleNotFoundError) as error:
        support.is_quantity()("quantity", None)

    assert error.value is failure
    assert support.puw is None
