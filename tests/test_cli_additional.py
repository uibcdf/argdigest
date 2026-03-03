import argparse
import types

import pytest

from argdigest.cli import audit_module, main


def test_audit_module_import_error(capsys, monkeypatch):
    def _boom(_name):
        raise ImportError("missing")

    monkeypatch.setattr("argdigest.cli.importlib.import_module", _boom)

    audit_module("missing.module")
    out, _ = capsys.readouterr()
    assert "Could not import module 'missing.module'" in out


def test_audit_module_reports_digestion_plan(capsys, monkeypatch):
    module = types.ModuleType("fake_module")

    def decorated():
        return None

    decorated.digestion_plan = argparse.Namespace(
        strictness="warn",
        skip_param="skip_digestion",
        profiling=False,
        digesters={"selection": object()},
        pipeline_targets={"syntax": {"kind": "std", "rules": ["is_str"]}},
    )
    module.decorated = decorated

    monkeypatch.setattr("argdigest.cli.importlib.import_module", lambda _name: module)

    audit_module("fake.module")
    out, _ = capsys.readouterr()
    assert "Audit Report for module: fake.module" in out
    assert "Function: decorated" in out
    assert "Argument Digesters: ['selection']" in out
    assert "kind='std'" in out


def test_cli_main_prints_help_without_command(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["argdigest"])
    main()
    out, _ = capsys.readouterr()
    assert "Available commands" in out


def test_cli_agent_error_path(capsys, monkeypatch):
    def _raise(_module):
        raise RuntimeError("generation failed")

    monkeypatch.setattr("sys.argv", ["argdigest", "agent", "init", "--module", "argdigest"])
    monkeypatch.setattr("argdigest.core.agent_docs.generate_agent_docs", _raise)
    main()

    out, _ = capsys.readouterr()
    assert "Error: generation failed" in out
