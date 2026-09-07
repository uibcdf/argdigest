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
