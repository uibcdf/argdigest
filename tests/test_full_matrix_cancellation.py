"""The full source matrix must remain cancellable after skipped dependencies."""

from pathlib import Path

import yaml


def test_full_matrix_uses_an_explicit_cancellable_status_guard():
    workflow = (
        Path(__file__).resolve().parents[1] / ".github/workflows/CI_full_matrix.yaml"
    )
    job = yaml.safe_load(workflow.read_text(encoding="utf-8"))["jobs"]["full-test"]
    condition = " ".join(job["if"].split())

    # An explicit status function also preserves execution when the decision
    # dependency is skipped or fails; an implicit success() would skip the job.
    assert condition.startswith("!cancelled() && ")
    assert "always()" not in condition
    assert job["needs"] == "nightly-decision"
    assert job["concurrency"]["cancel-in-progress"] is True
