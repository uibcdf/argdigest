"""Fresh processes distinguish catalog declarations from application policy."""

import json
import os
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

import pytest

from argdigest import diagnostics

PROBE = """
import importlib, json, logging, os, sys, warnings
import smonitor
from smonitor.handlers.memory import MemoryHandler
mode = os.environ['REGISTRATION_TEST_MODE']
configured = mode.startswith('configured')
handler = MemoryHandler()
if configured:
    smonitor.configure(level='DEBUG', profile='dev', handlers=[handler],
                       capture_logging=False, capture_warnings=False)
logging.getLogger().addHandler(logging.NullHandler())
manager = smonitor.get_manager()
config, hook = manager.config, warnings.showwarning
handlers = tuple(logging.getLogger().handlers)
manager_handlers = list(manager._handlers)
with smonitor.diagnostic_scope(safe_extra={'operation': 'registration-test'}):
    policy = smonitor.get_capture_policy()
    if mode == 'submodule':
        importlib.import_module('argdigest.core.config')
    from argdigest import (DigestConfig, arg_digest, register_diagnostics,
                           register_pipeline, configure_diagnostics)
    receipt = register_diagnostics()
    assert receipt['codes']
    assert register_diagnostics() == receipt
    @register_pipeline('registration-test', 'identity')
    def identity(value, ctx):
        return value
    @arg_digest(config=DigestConfig(argument_digestion=False),
                map={'value': {'kind': 'registration-test', 'rules': ['identity']}})
    def value(value):
        return value
    assert value('kept') == 'kept'
    @arg_digest(digestion_style='decorator', strictness='warn')
    def missing(unregistered_probe):
        return unregistered_probe
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        missing('kept')
    assert caught
    native = ValueError('DO_NOT_COLLECT_NATIVE_TEXT')
    def reject(value, ctx):
        raise native
    @arg_digest.map(value={'kind': 'registration-test', 'rules': [reject]})
    def failed(value):
        return value
    try:
        failed('kept')
    except ValueError as caught_error:
        assert caught_error is native
    else:
        raise AssertionError('Native failure must remain active')
    assert smonitor.get_capture_policy() == policy
    assert manager.config is config
    assert warnings.showwarning is hook
    assert tuple(logging.getLogger().handlers) == handlers
    assert manager._handlers == manager_handlers
    assert not any(n in sys.modules for n in ('numpy', 'pandas', 'pyunitwizard', 'beartype', 'pydantic'))
    if configured:
        assert any((event.get('code') or '').startswith('ARG-')
                   for event in handler.events)
        configure_diagnostics()
        assert manager.config is config
        if mode == 'configured_override':
            configure_diagnostics(use_provider_policy=True)
            assert manager.config is not config
            assert manager.config.profile == 'user'
            assert manager.config.level == 'WARNING'
    else:
        configure_diagnostics()
        assert manager.config is not config
print(json.dumps({'mode': mode, 'state': 'verified'}))
"""


@pytest.mark.parametrize(
    "mode", ["unconfigured", "configured", "configured_override", "submodule"]
)
def test_registration_execution_and_warnings_preserve_application_policy(request, mode):
    if not diagnostics._registration_only_available():
        if request.config.getoption("--require-registration-only"):
            pytest.fail("Qualification requires declaration-only SMonitor bundles")
        pytest.skip("Published provider lacks declaration-only bundle capability")
    environment = dict(os.environ, REGISTRATION_TEST_MODE=mode)
    with tempfile.TemporaryDirectory(prefix="argdigest-registration-test-") as cwd:
        result = subprocess.run(
            [sys.executable, "-P", "-c", PROBE],
            cwd=cwd,
            env=environment,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout.strip().splitlines()[-1])["state"] == "verified"


def test_old_provider_refuses_registration_only_but_keeps_explicit_bootstrap(
    monkeypatch,
):
    monkeypatch.setattr(diagnostics, "_registration_only_available", lambda: False)
    with pytest.raises(RuntimeError, match="bootstrap_policy=False"):
        diagnostics.register_diagnostics()
    calls = []
    monkeypatch.setattr(
        diagnostics.integrations,
        "ensure_configured",
        lambda root: calls.append(root),
    )
    diagnostics._initialize_diagnostics()
    assert calls == [diagnostics.PACKAGE_ROOT]


def test_explicit_bootstrap_rejects_nonboolean_policy_override():
    with pytest.raises(TypeError, match="boolean"):
        diagnostics.configure_diagnostics(use_provider_policy="False")


def test_unsupported_policy_override_refuses_before_configuration(monkeypatch):
    calls = []
    monkeypatch.setattr(
        diagnostics.integrations, "ensure_configured", lambda root: calls.append(root)
    )
    with pytest.raises(RuntimeError, match="cannot explicitly override policy"):
        diagnostics.configure_diagnostics(use_provider_policy=True)
    assert calls == []


def test_installed_qualification_refuses_unavailable_registration(tmp_path):
    """The real installed profile must fail rather than skip the feature gate."""
    root = Path(__file__).resolve().parents[1]
    profile = tomllib.loads((root / "devtools/conda-build/resources.toml").read_text())[
        "installed_tests"
    ]
    (tmp_path / "missing_registration_plugin.py").write_text(
        "def pytest_configure(config):\n"
        "    from argdigest import diagnostics\n"
        "    diagnostics._registration_only_available = lambda: False\n"
    )
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        [
            str(tmp_path),
            str(Path(diagnostics.__file__).resolve().parents[1]),
            environment.get("PYTHONPATH", ""),
        ]
    )
    node = (
        f"{Path(__file__).resolve()}::"
        "test_registration_execution_and_warnings_preserve_application_policy[unconfigured]"
    )
    result = subprocess.run(
        [
            sys.executable,
            "-P",
            "-m",
            "pytest",
            *profile["pytest_args"],
            "--import-mode=importlib",
            "-p",
            "no:cacheprovider",
            "-p",
            "missing_registration_plugin",
            node,
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Qualification requires declaration-only SMonitor bundles" in result.stdout
