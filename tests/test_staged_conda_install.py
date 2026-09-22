"""Exercise producer provenance and the staged-install release gate."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "devtools" / "conda-build" / "verify_staged_install.py"
WORKFLOW = ROOT / ".github" / "workflows" / "test_staged_conda_package.yaml"
SHA = "a" * 40
RUN_ID = 12345
DIGEST = "b" * 64

spec = importlib.util.spec_from_file_location("verify_staged_install", SCRIPT)
assert spec and spec.loader
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def _fixtures(tmp_path: Path) -> tuple[dict, Path]:
    run = {
        "id": RUN_ID,
        "event": "workflow_dispatch",
        "conclusion": "success",
        "head_sha": SHA,
        "path": verifier.PRODUCER_WORKFLOW,
        "run_attempt": 1,
    }
    route = {
        "schema": "argdigest.conda-route@1",
        "candidate_sha": SHA,
        "version": "0.11.0",
        "route": "staged",
        "gates": [{"workflow": ".github/workflows/CI_full_matrix.yaml", "run_id": 42}],
    }
    producer = {
        "schema": "gh-run-receptor.events@1",
        "subject": {
            "repository": "uibcdf/argdigest",
            "head_sha": SHA,
            "run_id": RUN_ID,
            "run_attempt": 1,
            "job_key": "conda_deployment_with_new_tag",
        },
        "events": [
            {
                "kind": "conda.package",
                "artifact": "argdigest-0.11.0-py_0.tar.bz2",
                "platform": "noarch",
                "build": "success",
                "upload": "success",
                "sha256": DIGEST,
            }
        ],
    }
    (tmp_path / "argdigest-conda-route.json").write_text(
        json.dumps(route), encoding="utf-8"
    )
    (tmp_path / "gh-run-receptor-events.json").write_text(
        json.dumps(producer), encoding="utf-8"
    )
    return run, tmp_path


def test_exact_producer_receipts_yield_expected_digest(tmp_path):
    run, evidence = _fixtures(tmp_path)
    assert verifier.verify_receipts(run, evidence, SHA, "0.11.0", 0, RUN_ID) == DIGEST


@pytest.mark.parametrize(
    ("surface", "field", "bad_value"),
    [
        ("run", "head_sha", "c" * 40),
        ("run", "conclusion", "failure"),
        ("run", "path", ".github/workflows/CI.yaml"),
        ("route", "route", "direct"),
        ("route", "version", "0.10.1"),
        ("producer", "sha256", "not-a-digest"),
        ("producer", "upload", "failure"),
        ("producer", "artifact", "argdigest-0.11.0-py_1.tar.bz2"),
    ],
)
def test_wrong_or_failed_producer_evidence_is_rejected(
    tmp_path, surface, field, bad_value
):
    run, evidence = _fixtures(tmp_path)
    if surface == "run":
        run[field] = bad_value
    else:
        filename = (
            "argdigest-conda-route.json"
            if surface == "route"
            else "gh-run-receptor-events.json"
        )
        path = evidence / filename
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if surface == "producer":
            receipt["events"][0][field] = bad_value
        else:
            receipt[field] = bad_value
        path.write_text(json.dumps(receipt), encoding="utf-8")
    with pytest.raises(ValueError):
        verifier.verify_receipts(run, evidence, SHA, "0.11.0", 0, RUN_ID)


def test_staged_matrix_checks_twelve_clean_installs_and_no_pip_source_install():
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    jobs = workflow["jobs"]
    assert jobs["install"]["needs"] == "verify-producer"
    matrix = jobs["install"]["strategy"]["matrix"]
    assert matrix["os"] == ["ubuntu-latest", "macos-latest", "windows-latest"]
    assert matrix["python"] == ["3.11", "3.12", "3.13", "3.14"]
    steps = jobs["install"]["steps"]
    setup = next(
        step for step in steps if step.get("name", "").startswith("Create a clean")
    )
    args = setup["with"]["create-args"]
    assert "channel_priority: flexible" in setup["with"]["condarc"]
    assert "uibcdf/label/staging::argdigest=" in args
    assert "uibcdf::depdigest=0.11.0=py_2" in args
    assert "uibcdf::smonitor=0.16.0=py_1" in args
    assert all("pip install" not in step.get("run", "") for step in steps)
    assert 'cd "$RUNNER_TEMP"' in steps[-1]["run"]
    assert "cygpath -u" in steps[-1]["run"]


@pytest.mark.parametrize(
    ("record_name", "field", "bad_value"),
    [
        (
            "argdigest",
            "url",
            "https://conda.anaconda.org/uibcdf/noarch/argdigest-0.11.0-py_0.tar.bz2",
        ),
        ("argdigest", "sha256", "c" * 64),
        ("smonitor", "url", f"{verifier.STAGING_CHANNEL}/smonitor-0.16.0-py_1.tar.bz2"),
        (
            "depdigest",
            "url",
            f"{verifier.STAGING_CHANNEL}/depdigest-0.11.0-py_2.tar.bz2",
        ),
    ],
)
def test_installed_gate_rejects_wrong_artifact_or_dependency_source(
    tmp_path, monkeypatch, record_name, field, bad_value
):
    _installed_fixture(tmp_path, monkeypatch, record_name, field, bad_value)

    with pytest.raises(ValueError):
        verifier.verify_installed(
            tmp_path,
            DIGEST,
            "0.13.0",
            0,
            f"{sys.version_info.major}.{sys.version_info.minor}",
        )


def test_installed_gate_accepts_exact_public_dependencies(tmp_path, monkeypatch):
    _installed_fixture(tmp_path, monkeypatch)
    verifier.verify_installed(
        tmp_path,
        DIGEST,
        "0.13.0",
        0,
        f"{sys.version_info.major}.{sys.version_info.minor}",
    )


def _installed_fixture(
    tmp_path, monkeypatch, record_name=None, field=None, bad_value=None
):
    meta = tmp_path / "conda-meta"
    meta.mkdir()
    package = {
        "name": "argdigest",
        "version": "0.13.0",
        "build": "py_0",
        "channel": verifier.STAGING_CHANNEL,
        "subdir": "noarch",
        "sha256": DIGEST,
        "url": f"{verifier.STAGING_CHANNEL}/argdigest-0.13.0-py_0.tar.bz2",
    }
    dependency = {
        "name": "smonitor",
        "version": "0.16.0",
        "build": "py_1",
        "channel": verifier.PUBLIC_CHANNEL,
        "url": "https://conda.anaconda.org/uibcdf/noarch/smonitor-0.16.0-py_1.tar.bz2",
    }
    depdigest = {
        "name": "depdigest",
        "version": "0.11.0",
        "build": "py_2",
        "channel": verifier.PUBLIC_CHANNEL,
        "url": "https://conda.anaconda.org/uibcdf/noarch/depdigest-0.11.0-py_2.tar.bz2",
    }
    records = {"argdigest": package, "smonitor": dependency, "depdigest": depdigest}
    if record_name is not None:
        records[record_name][field] = bad_value
    (meta / "argdigest-0.13.0-py_0.json").write_text(
        json.dumps(package), encoding="utf-8"
    )
    (meta / "smonitor-0.16.0-py_1.json").write_text(
        json.dumps(dependency), encoding="utf-8"
    )
    (meta / "depdigest-0.11.0-py_2.json").write_text(
        json.dumps(depdigest), encoding="utf-8"
    )
    monkeypatch.setattr(sys, "prefix", str(tmp_path))
    monkeypatch.setattr(verifier.importlib.metadata, "version", lambda _: "0.13.0")
    monkeypatch.setitem(
        sys.modules,
        "argdigest",
        SimpleNamespace(
            __version__="0.13.0", __file__=tmp_path / "argdigest" / "__init__.py"
        ),
    )
    monkeypatch.setattr(
        verifier.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stderr=""),
    )
