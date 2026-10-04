import re
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "devtools/conda-build/meta.yaml"
WORKFLOW = ROOT / ".github/workflows/build_and_upload_conda_packages.yaml"
PROMOTION_WORKFLOW = ROOT / ".github/workflows/promote_conda_package.yaml"
PIN = "5090a656cd8223826947575f329ee52aa664c725"


def test_recipe_declares_one_supported_noarch_python_artifact():
    recipe = RECIPE.read_text()
    assert "noarch: python" in recipe
    assert recipe.count("python >=3.11,<3.15") == 2
    assert "MOLSYSSUITE_CONDA_BUILD_NUMBER" in recipe
    build_script = (RECIPE.parent / "build.sh").read_text()
    assert "--no-deps --no-build-isolation" in build_script
    assert "  script:" not in recipe
    assert "freeze_project_version.py" not in build_script


def test_manual_candidates_are_exact_and_staging_only():
    workflow = WORKFLOW.read_text()
    assert "sha == os.environ['CANDIDATE_SHA']" in workflow
    assert "assert plan['route'] == 'staged'" in workflow
    jobs = yaml.safe_load(workflow)["jobs"]
    assert jobs["publish"]["needs"] == "decision"
    assert jobs["publish"]["uses"].endswith("@" + PIN)


def test_stable_releases_have_a_guarded_direct_route():
    workflow = WORKFLOW.read_text()
    assert "types: ['released']" in workflow
    job = yaml.safe_load(workflow)["jobs"]["publish"]
    assert "needs.decision.outputs.route == 'direct'" in job["if"]
    assert "publish-noarch-conda.yaml@" in job["uses"]
    assert "inputs.version || github.event.release.tag_name" in job["with"]["version"]


def test_staged_release_event_checks_plan_but_does_not_rebuild():
    workflow = WORKFLOW.read_text()
    assert "assert tag_sha == sha" in workflow
    assert "plan['route'] in ('staged', 'direct')" in workflow
    condition = yaml.safe_load(workflow)["jobs"]["publish"]["if"]
    # A release event with route=staged has no eligible build job.
    assert (
        condition
        == "github.event_name == 'workflow_dispatch' || needs.decision.outputs.route == 'direct'"
    )


def test_noarch_workflow_has_one_job_and_retains_producer_evidence():
    workflow = yaml.safe_load(WORKFLOW.read_text())
    job = workflow["jobs"]["publish"]
    assert (
        job["uses"]
        == f"uibcdf/molsyssuite/.github/workflows/publish-noarch-conda.yaml@{PIN}"
    )
    assert job["secrets"]["ANACONDA_TOKEN"] == "${{ secrets.ANACONDA_UIBCDF_TOKEN }}"
    inventory = tomllib.loads(
        (ROOT / "devtools/conda-build/resources.toml").read_text()
    )
    assert inventory["version_file"] in inventory["required_paths"]
    assert inventory["installed_tests"]["paths"] == ["tests"]


def test_promotion_workflow_checks_exact_release_and_file_identity():
    workflow = yaml.safe_load(PROMOTION_WORKFLOW.read_text())
    job = workflow["jobs"]["promote"]
    assert job["needs"] == "release"
    assert (
        job["uses"]
        == f"uibcdf/molsyssuite/.github/workflows/promote-noarch-conda.yaml@{PIN}"
    )
    assert job["with"]["installed_run_id"] == "${{ inputs.installed_run_id }}"
    assert job["with"]["sha256"] == "${{ inputs.sha256 }}"
    guard = (ROOT / "devtools/conda-build/verify_core_release.py").read_text()
    assert "refs/heads/main" in guard
    assert "releases/tags/" in guard


def test_source_gate_declares_every_executed_matrix_cell():
    plan = tomllib.loads((ROOT / "devtools/conda-build/release_plan.toml").read_text())
    matrix = yaml.safe_load(
        (ROOT / ".github/workflows/CI_full_matrix.yaml").read_text()
    )["jobs"]["full-test"]["strategy"]["matrix"]["cfg"]
    expected = {
        f"Full test on {cell['os']}, Python {cell['python-version']}" for cell in matrix
    }
    assert set(plan["gate_jobs"][".github/workflows/CI_full_matrix.yaml"]) == expected
    assert all(
        steps == ["Run tests"]
        for steps in plan["gate_jobs"][".github/workflows/CI_full_matrix.yaml"].values()
    )
    for job in yaml.safe_load(
        (ROOT / ".github/workflows/verify_zenodo_releases.yaml").read_text()
    )["jobs"].values():
        assert re.fullmatch(r"[0-9a-f]{40}", job["uses"].rsplit("@", 1)[1])
        assert job["with"]["since"] == "2026-10-04T00:00:00Z"
