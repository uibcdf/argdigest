from __future__ import annotations

import re
import tomllib
from pathlib import Path

#: The Python versions ArgDigest supports, and the platforms each one is tested on.
#: Everything else in this file is derived from these three constants, so widening or
#: narrowing support is one edit here plus the files the tests then point at.
SUPPORTED_PYTHON = ("3.11", "3.12", "3.13")
SUPPORTED_PLATFORMS = ("ubuntu-latest", "macos-latest")

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _pyproject() -> dict:
    return tomllib.loads(_read("pyproject.toml"))


def _expected_requires_python() -> str:
    """The range implied by the versions actually tested.

    Closed at both ends on purpose. An open upper bound would promise support for a
    Python that has never been run against, which is the promise `requires-python` is
    least able to keep: a release that predates the interpreter cannot have been tested
    on it.
    """

    minors = sorted(int(version.split(".")[1]) for version in SUPPORTED_PYTHON)
    return f">=3.{minors[0]},<3.{minors[-1] + 1}"


def test_the_declared_range_matches_the_versions_actually_tested():
    assert _expected_requires_python() == ">=3.11,<3.14"


def test_pyproject_declares_the_supported_python_range():
    assert _pyproject()["project"]["requires-python"] == _expected_requires_python()


def test_full_matrix_tests_every_supported_python_on_every_platform():
    """The full matrix is what makes the declared range true rather than aspirational."""

    text = _read(".github/workflows/CI_full_matrix.yaml")
    cells = set(re.findall(
        r"os:\s*([\w.-]+)\s*,\s*python-version:\s*\"([\d.]+)\"", text))

    assert cells == {
        (platform, version)
        for platform in SUPPORTED_PLATFORMS
        for version in SUPPORTED_PYTHON
    }


def test_fast_gate_runs_a_cell_of_the_supported_matrix():
    """The per-push gate may test one combination, but not an unsupported one."""

    text = _read(".github/workflows/CI.yaml")
    versions = set(re.findall(r"python-version:\s*\"([\d.]+)\"", text))
    versions |= set(re.findall(r"python=([\d.]+)", text))

    assert versions
    assert versions <= set(SUPPORTED_PYTHON)


def test_conda_packages_are_built_for_every_supported_python():
    text = _read(".github/workflows/build_and_upload_conda_packages.yaml")
    declared = re.search(r"python-version:\s*\[([^\]]+)\]", text)

    assert declared is not None
    assert tuple(re.findall(r"\"([\d.]+)\"", declared.group(1))) == SUPPORTED_PYTHON


def test_readme_badge_lists_the_supported_pythons():
    badge = "%20%7C%20".join(SUPPORTED_PYTHON)

    assert f"Python-{badge}-blue" in _read("README.md")


def test_pyproject_declares_minimum_sibling_versions():
    data = _pyproject()
    deps = data["project"]["dependencies"]

    assert "smonitor>=0.11.4" in deps
    assert "depdigest>=0.9.1" in deps

    extras = data["project"]["optional-dependencies"]
    assert "pyunitwizard>=0.11.0" in extras["pyunitwizard"]
    assert "pyunitwizard>=0.11.0" in extras["all"]


def test_docs_compatibility_matrix_mentions_expected_versions():
    text = _read("docs/content/developer/compatibility-matrix.md")

    assert re.search(r"`smonitor`\s*\|\s*`0\.11\.4`", text)
    assert re.search(r"`depdigest`\s*\|\s*`0\.9\.1`", text)
    assert re.search(r"`pyunitwizard`\s*\|\s*`0\.11\.0`", text)


def test_docs_compatibility_matrix_states_the_python_range_and_platforms():
    text = _read("docs/content/developer/compatibility-matrix.md")

    assert _expected_requires_python() in text
    for version in SUPPORTED_PYTHON:
        assert re.search(rf"\|\s*`{re.escape(version)}`\s*\|\s*tested\s*\|\s*tested\s*\|", text), (
            f"the matrix page does not show {version} as tested on both platforms")
