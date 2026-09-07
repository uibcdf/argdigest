from __future__ import annotations

import importlib
import sys

from argdigest.core.context import Context
from argdigest.core.errors import DigestNotDigestedWarning, DigestTypeError
from argdigest.core.registry import Registry, get_pipelines


def test_catalog_errors_expose_code_and_hint_fields():
    """`hint` comes from the catalog now, not from the raise site.

    It used to be whatever the raise site passed as `hint=`. That parameter is
    gone: the wording belongs to the catalog, and SMonitor exposes it as a
    derived property re-resolved from `code` and `extra` (uibcdf/smonitor#5).
    What the test is for -- a catalog error carries its code and its hint as
    fields, rather than fused into prose a caller has to parse -- is unchanged.
    """
    ctx = Context(function_name="f", argname="x", value="bad", all_args={})
    exc = DigestTypeError(context=ctx, detail="Expected an int.")

    assert exc.code == "ARG-ERR-TYPE-001"
    assert (
        exc.hint
        == "Check the type this argument expects. See https://www.uibcdf.org/argdigest."
    )
    assert "Expected an int." in str(exc)


def test_catalog_warning_exposes_code_and_hint_fields():
    ctx = Context(function_name="f", argname="x", value="bad", all_args={})
    warning = DigestNotDigestedWarning(context=ctx)

    assert warning.code == "ARG-WARN-MISS-001"
    assert warning.hint == (
        "Define or register a digester for 'x'. See https://www.uibcdf.org/argdigest."
    )


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
