"""A green minimal-core probe may not substitute for an executed matrix."""

import copy
import importlib.util
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[1] / "devtools/conda-build/verify_core_release.py"
)
spec = importlib.util.spec_from_file_location("core_release_gate", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def fixture():
    plan = {
        "test_platforms": ["linux-64", "osx-arm64", "win-64"],
        "python_versions": ["3.11", "3.12", "3.13", "3.14"],
    }
    run = {
        "head_sha": "a" * 40,
        "display_title": "exact file and digest",
        "path": gate.WORKFLOW,
        "status": "completed",
        "conclusion": "success",
        "run_attempt": 1,
    }
    jobs = [
        {
            "name": f"Core {os} / Python {python}",
            "run_attempt": 1,
            "status": "completed",
            "conclusion": "success",
            "steps": [
                {"name": gate.STEP, "status": "completed", "conclusion": "success"}
            ],
        }
        for os in ("ubuntu-latest", "macos-latest", "windows-latest")
        for python in plan["python_versions"]
    ]
    return run, jobs, plan


def test_core_gate_accepts_complete_executed_matrix():
    run, jobs, plan = fixture()
    gate.validate_run(run, jobs, "a" * 40, "exact file and digest", plan)


@pytest.mark.parametrize(
    "failure",
    [
        "missing",
        "duplicate",
        "skipped_job",
        "skipped_step",
        "wrong_attempt",
        "wrong_source",
        "wrong_digest",
    ],
)
def test_core_gate_rejects_incomplete_or_unexecuted_evidence(failure):
    run, jobs, plan = fixture()
    if failure == "missing":
        jobs.pop()
    elif failure == "duplicate":
        jobs[-1] = copy.deepcopy(jobs[0])
    elif failure == "skipped_job":
        jobs[0]["conclusion"] = "skipped"
    elif failure == "skipped_step":
        jobs[0]["steps"][0]["conclusion"] = "skipped"
    elif failure == "wrong_attempt":
        jobs[0]["run_attempt"] = 2
    elif failure == "wrong_source":
        run["head_sha"] = "b" * 40
    elif failure == "wrong_digest":
        run["display_title"] = "another digest"
    with pytest.raises(AssertionError):
        gate.validate_run(run, jobs, "a" * 40, "exact file and digest", plan)
