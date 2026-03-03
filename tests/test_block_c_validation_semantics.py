from __future__ import annotations

import importlib
import warnings
from textwrap import dedent

import pytest
import smonitor

from argdigest import arg_digest
from argdigest.contrib import pyunitwizard_support as puw_support
from argdigest.core.context import Context
from argdigest.core.errors import DigestNotDigestedWarning, DigestValueError


def test_smonitor_profile_user_vs_dev_message_shape():
    ctx = Context(function_name="f", argname="x", value="bad", all_args={})
    try:
        smonitor.configure(profile="user")
        user_msg = str(DigestValueError("invalid", context=ctx, hint="set a valid value"))
        smonitor.configure(profile="dev")
        dev_msg = str(DigestValueError("invalid", context=ctx, hint="set a valid value"))
    finally:
        smonitor.configure(profile="user")

    assert "Check the valid values" in user_msg
    assert "Validate value constraints" in dev_msg
    assert user_msg != dev_msg


def test_pyunitwizard_conversion_error_keeps_caller_context(monkeypatch):
    class FakePuw:
        @staticmethod
        def convert(_value, to_unit=None, to_form=None):
            raise RuntimeError(f"cannot convert to {to_unit}")

    monkeypatch.setattr(puw_support, "HAS_PUW", True)
    monkeypatch.setattr(puw_support, "puw", FakePuw)

    ctx = Context(function_name="my_pkg.api.get", argname="dist", value="bad", all_args={})
    with pytest.raises(DigestValueError) as excinfo:
        puw_support.convert(to_unit="nm")("bad", ctx)

    exc = excinfo.value
    assert exc.context.function_name == "my_pkg.api.get"
    assert exc.context.argname == "dist"
    assert exc.code == "ARG-ERR-VAL-001"


def test_strictness_aliases_and_ignore_behavior():
    @arg_digest(digestion_style="decorator", strictness="silent")
    def f(a):
        return a

    with warnings.catch_warnings(record=True) as record:
        warnings.simplefilter("always")
        assert f("x") == "x"
        assert record == []


def test_invalid_strictness_value_raises():
    with pytest.raises(ValueError, match="strictness must be one of"):
        @arg_digest(digestion_style="decorator", strictness="boom")
        def f(a):
            return a

        f("x")


def test_warning_taxonomy_consistent_across_package_and_registry_styles(tmp_path, monkeypatch):
    # Package style: mock_molsysmt only digests "selection", so "other" should warn.
    @arg_digest(config="tests.mock_molsysmt._argdigest", strictness="warn")
    def f_pkg(selection, other):
        return selection, other

    with pytest.warns(DigestNotDigestedWarning):
        f_pkg("protein", 1)

    # Registry style: provide one digester only, second arg should warn with same warning class.
    pkg_dir = tmp_path / "regstylepkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
    (pkg_dir / "registry.py").write_text(
        dedent(
            """
            def digest_a(a, caller=None):
                return int(a)

            ARGUMENT_DIGESTERS = {"a": digest_a}
            """
        ),
        encoding="utf-8",
    )
    (pkg_dir / "_argdigest.py").write_text(
        dedent(
            """
            DIGESTION_SOURCE = "regstylepkg.registry"
            DIGESTION_STYLE = "registry"
            STRICTNESS = "warn"
            """
        ),
        encoding="utf-8",
    )
    (pkg_dir / "api.py").write_text(
        dedent(
            """
            from argdigest import arg_digest

            @arg_digest(config="regstylepkg._argdigest")
            def f_reg(a, b):
                return a, b
            """
        ),
        encoding="utf-8",
    )

    monkeypatch.syspath_prepend(str(tmp_path))
    api = importlib.import_module("regstylepkg.api")
    with pytest.warns(DigestNotDigestedWarning):
        out_a, out_b = api.f_reg("3", "x")
        assert out_a == 3
        assert out_b == "x"
