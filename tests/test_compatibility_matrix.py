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


def _requirement_name(requirement: str) -> str:
    """The distribution name of a requirement string, lowercased."""

    return re.split(r"[<>=!~\[; ]", requirement.strip(), maxsplit=1)[0].lower()


def _declared_floors(requirements: list[str]) -> dict[str, str | None]:
    """Map each requirement to the lower bound it declares, or `None` if it declares none.

    Parsed with a regular expression rather than `packaging` so this file keeps to the
    standard library, as the rest of it does.
    """

    floors: dict[str, str | None] = {}
    for requirement in requirements:
        match = re.search(r">=\s*([\w.]+)", requirement)
        floors[_requirement_name(requirement)] = match.group(1) if match else None
    return floors


def _runtime_floors() -> dict[str, str | None]:
    """The hard runtime dependency floors, read from the packaging authority.

    `pyproject.toml` is where a Python distribution declares what it needs. Everything
    else that repeats those numbers -- the conda recipe, the documented matrix -- is
    checked against this rather than against a version typed into a test. A floor typed
    in three places is three places to forget, and forgetting one of them is exactly the
    drift these tests exist to catch.
    """

    return _declared_floors(_pyproject()["project"]["dependencies"])


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
    """Every dependency carries a lower bound; which bound is the manifest's business.

    An unbounded sibling is what makes an installation resolvable into a combination
    nobody tested, and the failure is silent: the resolver reports success. This asserts
    that the bound exists, not that it equals a number this file would then have to be
    edited to change.
    """

    data = _pyproject()

    for name, floor in _runtime_floors().items():
        assert floor is not None, f"{name} is declared without a lower bound"

    extras = data["project"]["optional-dependencies"]
    for extra in ("pyunitwizard", "all"):
        floors = _declared_floors(extras[extra])
        assert floors.get("pyunitwizard") is not None, (
            f"pyunitwizard is unbounded in the {extra!r} extra")

    assert _declared_floors(extras["pyunitwizard"])["pyunitwizard"] == \
        _declared_floors(extras["all"])["pyunitwizard"], (
        "the pyunitwizard extra and the all extra declare different floors")


def test_conda_recipe_matches_the_hard_runtime_dependency_set():
    """The recipe and `pyproject.toml` are two statements of one contract.

    Compared in both directions, and against each other rather than against a literal:
    a floor raised in one manifest and not the other is the defect, and a floor raised
    in both is an ordinary change that must not turn this red.
    """

    text = _read("devtools/conda-build/meta.yaml")
    run_block = re.search(r"(?m)^  run:\n(?P<body>(?:    - .*\n)+)", text)
    assert run_block is not None, "the conda recipe has no requirements.run block"

    recipe = _declared_floors([
        line.strip()[2:] for line in run_block.group("body").splitlines()
        if line.strip().startswith("- ")
    ])
    recipe.pop("python", None)

    assert recipe == _runtime_floors(), (
        "the conda recipe and pyproject.toml declare different runtime dependencies "
        f"or floors: recipe={recipe}, pyproject={_runtime_floors()}")

    for optional_dependency in ("beartype", "pydantic", "pyunitwizard", "pandas"):
        assert f"- {optional_dependency}" not in text

    assert re.search(r"test:\s+imports:\s+- argdigest", text)


def test_docs_compatibility_matrix_mentions_expected_versions():
    """The documented matrix states the floors the manifests declare.

    This is the row that went stale unnoticed when the smonitor floor was raised: the
    page and the test held the same superseded number, so they agreed with each other
    and with nothing else.
    """

    text = _read("docs/content/developer/compatibility-matrix.md")
    documented = dict(re.findall(r"\|\s*`([\w-]+)`\s*\|\s*`([\w.]+)`\s*\|", text))

    for name, floor in _runtime_floors().items():
        if name == "numpy":
            continue
        assert documented.get(name) == floor, (
            f"the matrix page documents {name} {documented.get(name)!r}, "
            f"the manifests declare {floor!r}")

    extras = _pyproject()["project"]["optional-dependencies"]
    assert documented.get("pyunitwizard") == \
        _declared_floors(extras["pyunitwizard"])["pyunitwizard"]


def test_docs_compatibility_matrix_states_the_python_range_and_platforms():
    text = _read("docs/content/developer/compatibility-matrix.md")

    assert _expected_requires_python() in text
    for version in SUPPORTED_PYTHON:
        assert re.search(rf"\|\s*`{re.escape(version)}`\s*\|\s*tested\s*\|\s*tested\s*\|", text), (
            f"the matrix page does not show {version} as tested on both platforms")
