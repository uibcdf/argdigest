from __future__ import annotations

import re
import tomllib
from pathlib import Path


def test_pyproject_declares_minimum_sibling_versions():
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    deps = data["project"]["dependencies"]

    assert "smonitor>=0.11.4" in deps
    assert "depdigest>=0.9.1" in deps

    extras = data["project"]["optional-dependencies"]
    assert "pyunitwizard>=0.11.0" in extras["pyunitwizard"]
    assert "pyunitwizard>=0.11.0" in extras["all"]


def test_docs_compatibility_matrix_mentions_expected_versions():
    text = Path("docs/content/developer/compatibility-matrix.md").read_text(encoding="utf-8")

    assert re.search(r"`smonitor`\s*\|\s*`0\.11\.4`", text)
    assert re.search(r"`depdigest`\s*\|\s*`0\.9\.1`", text)
    assert re.search(r"`pyunitwizard`\s*\|\s*`0\.11\.0`", text)
