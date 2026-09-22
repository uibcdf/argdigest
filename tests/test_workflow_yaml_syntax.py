"""Reject malformed workflow YAML before GitHub ignores its dispatch trigger."""

from pathlib import Path

import pytest
import yaml

WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"


@pytest.mark.parametrize(
    "workflow",
    sorted(path for path in WORKFLOWS.iterdir() if path.suffix in {".yaml", ".yml"}),
)
def test_workflow_yaml_is_a_mapping_with_jobs(workflow):
    document = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    assert isinstance(document, dict), workflow
    assert isinstance(document.get("jobs"), dict), workflow
