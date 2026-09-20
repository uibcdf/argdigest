from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from devtools import devguide_reports

ROOT = Path(__file__).resolve().parents[1]


def test_report_metadata_and_lifecycle_are_valid():
    _, errors = devguide_reports.validate_all()

    assert errors == []


def test_generated_report_indexes_are_current():
    completed = subprocess.run(
        [sys.executable, "devtools/devguide_index.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_local_protocol_routes_to_the_suite_contract():
    protocol = (ROOT / "devguide/reporting_protocol.md").read_text(encoding="utf-8")

    assert "uibcdf/molsyssuite#11" in protocol
    assert "pending_bugs" in protocol
    assert "pending_proposals" in protocol
    assert "Archive, never delete" in protocol


def test_pytest_guard_rejects_a_missing_file(tmp_path):
    errors = devguide_reports.validate_pytest_guard(tmp_path, "tests/test_missing.py")

    assert any("file that does not exist" in error for error in errors)


def test_pytest_guard_rejects_a_missing_node_and_parameter_id(tmp_path):
    test_file = tmp_path / "tests/test_example.py"
    test_file.parent.mkdir()
    test_file.write_text("def test_present():\n    pass\n", encoding="utf-8")

    missing = devguide_reports.validate_pytest_guard(
        tmp_path, "tests/test_example.py::test_absent"
    )
    parameterized = devguide_reports.validate_pytest_guard(
        tmp_path, "tests/test_example.py::test_present[param]"
    )

    assert any("does not resolve" in error for error in missing)
    assert any(
        "parameterized selectors are not supported" in error for error in parameterized
    )


def test_pytest_guard_accepts_a_module_function_and_class_method(tmp_path):
    test_file = tmp_path / "tests/test_example.py"
    test_file.parent.mkdir()
    test_file.write_text(
        "def test_function():\n"
        "    pass\n\n"
        "class TestGroup:\n"
        "    def test_method(self):\n"
        "        pass\n",
        encoding="utf-8",
    )

    for selector in (
        "tests/test_example.py",
        "tests/test_example.py::test_function",
        "tests/test_example.py::TestGroup::test_method",
    ):
        assert devguide_reports.validate_pytest_guard(tmp_path, selector) == []
