from __future__ import annotations

import importlib
from textwrap import dedent

from argdigest import arg_digest, argument_digest
from argdigest.core.config import DigestConfig


def test_runtime_config_overrides_env_config(monkeypatch):
    monkeypatch.setenv("ARGDIGEST_CONFIG", "tests.mock_molsysmt._argdigest")

    @argument_digest("selection")
    def digest_selection(selection, caller=None):
        return f"decorator:{selection}"

    @arg_digest(config=DigestConfig(digestion_style="decorator", strictness="ignore"))
    def f(selection):
        return selection

    assert f("A") == "decorator:A"


def test_env_config_overrides_auto_module_config(tmp_path, monkeypatch):
    pkg_dir = tmp_path / "tmpautopkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
    (pkg_dir / "_argdigest.py").write_text(
        dedent(
            """
            DIGESTION_STYLE = "decorator"
            STRICTNESS = "ignore"
            """
        ),
        encoding="utf-8",
    )
    (pkg_dir / "api.py").write_text(
        dedent(
            """
            from argdigest import arg_digest

            @arg_digest()
            def f(selection):
                return selection
            """
        ),
        encoding="utf-8",
    )

    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.setenv("ARGDIGEST_CONFIG", "tests.mock_molsysmt._argdigest")

    api = importlib.import_module("tmpautopkg.api")
    assert api.f("protein") == "Selection: protein, Syntax: None"
