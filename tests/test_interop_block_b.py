from __future__ import annotations

import importlib
import sys

from argdigest.core.context import Context
from argdigest.core.errors import DigestTypeError, DigestNotDigestedWarning
from argdigest.core.registry import Registry, get_pipelines


def test_catalog_errors_expose_code_and_hint_fields():
    ctx = Context(function_name="f", argname="x", value="bad", all_args={})
    exc = DigestTypeError("boom", context=ctx, hint="fix this")

    assert exc.code == "ARG-ERR-TYPE-001"
    assert exc.hint == "fix this"


def test_catalog_warning_exposes_code_and_hint_fields():
    ctx = Context(function_name="f", argname="x", value="bad", all_args={})
    warning = DigestNotDigestedWarning("missing", context=ctx, hint="add digester")

    assert warning.code == "ARG-WARN-MISS-001"
    assert warning.hint == "add digester"


def test_registry_entrypoints_are_smonitor_instrumented():
    assert hasattr(Registry.run, "__wrapped__")
    assert hasattr(get_pipelines, "__wrapped__")


def test_optional_contrib_modules_import_without_hard_optional_deps(monkeypatch):
    original_import = __import__

    def _import(name, *args, **kwargs):
        if name == "beartype":
            raise ImportError("beartype unavailable")
        if name == "pydantic":
            raise ImportError("pydantic unavailable")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", _import)

    sys.modules.pop("argdigest.contrib.beartype_support", None)
    sys.modules.pop("argdigest.contrib.pydantic_support", None)
    beartype_mod = importlib.import_module("argdigest.contrib.beartype_support")
    pydantic_mod = importlib.import_module("argdigest.contrib.pydantic_support")

    assert hasattr(beartype_mod, "beartype_digest")
    assert hasattr(pydantic_mod, "pydantic_pipeline")
