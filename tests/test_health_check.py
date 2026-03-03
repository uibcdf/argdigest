from __future__ import annotations

from argdigest.cli import main
from argdigest.core.health import run_health_check


def test_run_health_check_contract():
    report = run_health_check()
    expected = {"smonitor", "depdigest", "pyunitwizard_optional", "diagnostics", "profiles"}
    assert set(report.keys()) == expected
    for item in report.values():
        assert "ok" in item
        assert "detail" in item


def test_cli_health_check_command(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["argdigest", "health-check"])
    main()
    out, _ = capsys.readouterr()
    assert "ArgDigest ecosystem health check" in out
    assert "- smonitor:" in out
    assert "- depdigest:" in out
