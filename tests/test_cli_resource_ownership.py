"""Real CLI test nodes must preserve the caller's files on success and failure."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

CLI_TESTS = Path(__file__).with_name("test_cli.py")
FAILURE_PLUGIN = """
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    from argdigest.core import agent_docs
    original = agent_docs.generate_agent_docs
    def fail_after_write(*args, **kwargs):
        original(*args, **kwargs)
        raise RuntimeError("CONTROLLED_CLI_FAILURE_AFTER_WRITE")
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(agent_docs, "generate_agent_docs", fail_after_write)
        yield
"""


@pytest.mark.parametrize("node", ["test_cli_agent_init_real", "test_cli_agent_update"])
@pytest.mark.parametrize("failed", [False, True])
def test_real_cli_tests_preserve_caller_files_and_retire_outputs(node, failed):
    with tempfile.TemporaryDirectory(prefix="argdigest-cli-custody-") as workspace:
        root = Path(workspace)
        sentinel = root / "ARG_DIGEST_AGENTS.md"
        content = b"Caller-owned instructions: keep these exact bytes.\n"
        sentinel.write_bytes(content)
        scratch = root / "child-temporary"
        scratch.mkdir()
        environment = dict(os.environ)
        environment.update(TMPDIR=str(scratch), TEMP=str(scratch), TMP=str(scratch))
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        command = [
            sys.executable,
            "-m",
            "pytest",
            "--receptor=ci",
            "-q",
            "-p",
            "no:cacheprovider",
            "--basetemp",
            str(root / "pytest-fixtures"),
            f"{CLI_TESTS}::{node}",
        ]
        if failed:
            (root / "custody_failure_plugin.py").write_text(FAILURE_PLUGIN)
            environment["PYTHONPATH"] = os.pathsep.join(
                filter(None, (str(root), environment.get("PYTHONPATH", "")))
            )
            command.extend(["-p", "custody_failure_plugin"])
        result = subprocess.run(
            command,
            cwd=root,
            env=environment,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        assert result.returncode == (1 if failed else 0), result.stdout + result.stderr
        if failed:
            assert "CONTROLLED_CLI_FAILURE_AFTER_WRITE" in result.stdout, result.stdout
        assert sentinel.read_bytes() == content
        assert list(scratch.iterdir()) == []
    assert not root.exists()
