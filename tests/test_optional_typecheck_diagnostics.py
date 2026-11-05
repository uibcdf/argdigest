"""Real providers distinguish optional absence from broken and required imports."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import argdigest

PROBE = """
import importlib.abc, importlib.machinery, json, sys
mode = sys.argv[1]
class Broken(importlib.abc.Loader):
    def create_module(self, spec): return None
    def exec_module(self, module):
        if mode == "transitive":
            raise ModuleNotFoundError("missing transitive dependency", name="missing_transitive")
        raise ImportError("BROKEN_BEARTYPE")
class Finder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "beartype":
            if mode in ("absent", "required"):
                raise ModuleNotFoundError("controlled absence", name="beartype")
            return importlib.machinery.ModuleSpec(fullname, Broken())
sys.meta_path.insert(0, Finder())
import smonitor
from smonitor.handlers.memory import MemoryHandler
handler = MemoryHandler()
smonitor.configure(level="DEBUG", handlers=[handler], capture_logging=False, capture_warnings=False)
from argdigest import arg_digest, DigestConfig
if mode == "required":
    from depdigest import check_dependency
    try:
        check_dependency("beartype")
    except ImportError:
        pass
    else:
        raise AssertionError("Required dependency did not refuse absence")
else:
    try:
        for index in range(2):
            @arg_digest(type_check=True, config=DigestConfig(argument_digestion=False))
            def target(value): return value
            assert target(3) == target(3) == 3
    except ImportError as error:
        assert mode in ("broken", "transitive"), (mode, error)
        assert str(error) == ("BROKEN_BEARTYPE" if mode == "broken" else "missing transitive dependency")
    else:
        assert mode == "absent", "Broken optional engine was silently disabled"
events = [{"code": event.get("code"), "level": event.get("level")} for event in handler.events]
codes = [event["code"] for event in events]
if mode == "absent":
    assert codes.count("ARG-WARN-TYPECHECK-001") == 2, events
    assert "DEP-ERR-MISS-001" not in codes, events
    assert "beartype" not in sys.modules
elif mode == "required":
    assert "DEP-ERR-MISS-001" in codes, events
else:
    assert "ARG-WARN-TYPECHECK-001" not in codes, events
print(json.dumps({"mode": mode, "events": events}))
"""


@pytest.mark.parametrize("mode", ["absent", "broken", "transitive", "required"])
def test_optional_typecheck_diagnostics_in_fresh_process(tmp_path, mode):
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(Path(argdigest.__file__).resolve().parents[1])
    result = subprocess.run(
        [sys.executable, "-c", PROBE, mode],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout.splitlines()[-1])["mode"] == mode
