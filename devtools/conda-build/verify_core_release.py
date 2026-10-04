"""Fail closed on public release identity and minimal-core matrix evidence."""

from __future__ import annotations

import json
import os
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ".github/workflows/test_staged_core_conda_package.yaml"
STEP = "Verify exact installed core without NumPy"


def get(path: str):
    return json.loads(
        subprocess.check_output(["gh", "api", path], text=True, timeout=30)
    )


def validate_run(run: dict, jobs: list[dict], sha: str, title: str, plan: dict):
    assert run["head_sha"] == sha
    assert run["display_title"] == title
    assert run["path"] == WORKFLOW
    assert run["status"] == "completed" and run["conclusion"] == "success"
    runners = {
        "linux-64": "ubuntu-latest",
        "osx-arm64": "macos-latest",
        "win-64": "windows-latest",
    }
    expected = {
        f"Core {runners[platform]} / Python {python}"
        for platform in plan["test_platforms"]
        for python in plan["python_versions"]
    }
    assert len(jobs) == len(expected) and {job["name"] for job in jobs} == expected
    for job in jobs:
        assert job["run_attempt"] == run["run_attempt"]
        assert job["status"] == "completed" and job["conclusion"] == "success"
        steps = [step for step in job["steps"] if step["name"] == STEP]
        assert len(steps) == 1
        assert steps[0]["status"] == "completed" and steps[0]["conclusion"] == "success"


def main():
    assert os.environ["GITHUB_REF"] == "refs/heads/main"
    assert os.environ["GITHUB_REPOSITORY"] == "uibcdf/argdigest"
    sha, version, digest = (
        os.environ[name] for name in ("CANDIDATE_SHA", "VERSION", "SHA256")
    )
    assert (
        subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == sha
    )
    assert (
        subprocess.check_output(
            ["git", "rev-list", "-n", "1", version], text=True
        ).strip()
        == sha
    )
    release = get(f"repos/uibcdf/argdigest/releases/tags/{version}")
    assert (
        release["tag_name"] == version
        and not release["draft"]
        and not release["prerelease"]
    )
    plan = tomllib.loads((ROOT / "devtools/conda-build/release_plan.toml").read_text())
    assert version == plan["version"]
    title = (
        f"Core installed argdigest-{version}-py_{plan['build_number']}.tar.bz2 {digest}"
    )
    endpoint = f"repos/uibcdf/argdigest/actions/runs/{os.environ['CORE_RUN_ID']}"
    run = get(endpoint)
    page = get(f"{endpoint}/attempts/{run['run_attempt']}/jobs?per_page=100")
    assert page["total_count"] == len(page["jobs"]), "Incomplete jobs inventory"
    validate_run(run, page["jobs"], sha, title, plan)
    current = get(endpoint)
    assert (
        current["run_attempt"] == run["run_attempt"]
        and current["conclusion"] == "success"
    )
    print("PASS: exact public release and executed minimal-core installed matrix")


if __name__ == "__main__":
    main()
