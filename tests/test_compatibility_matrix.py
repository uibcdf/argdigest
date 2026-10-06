from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest
import yaml
from packaging.version import Version

#: The Python versions ArgDigest supports, and the platforms each one is tested on.
#: Compatibility assertions derive their supported matrix from these constants;
#: provider floors derive from packaging metadata and environment roles below.
SUPPORTED_PYTHON = ("3.11", "3.12", "3.13", "3.14")
SUPPORTED_PLATFORMS = ("ubuntu-latest", "macos-latest", "windows-latest")

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_ENVIRONMENTS = (
    "development_env.yaml",
    "docs_env.yaml",
    "test_env.yaml",
    "test_env_core.yaml",
)
BUILD_ONLY_ENVIRONMENTS = ("build_env.yaml",)


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _pyproject() -> dict:
    return tomllib.loads(_read("pyproject.toml"))


def _requirement_name(requirement: str) -> str:
    """The distribution name of a requirement string, lowercased."""

    return re.split(r"[<>=!~\[; ]", requirement.strip(), maxsplit=1)[0].lower()


def _declared_floors(requirements: list[str]) -> dict[str, str | None]:
    """Map each requirement to the lower bound it declares, or `None` if it declares none.

    This bounded parser covers the explicit >= constraints used in the reviewed
    manifests. Environment comparisons use packaging for version ordering.
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


def _environment_requirements(name: str) -> list[str]:
    document = yaml.safe_load(_read(f"devtools/conda-envs/{name}"))
    return [item for item in document["dependencies"] if isinstance(item, str)]


def _assert_environment_floors(requirements: list[str], route: str) -> None:
    """Protect required provider floors; stricter environment floors remain valid."""
    observed = _declared_floors(requirements)
    for name, expected in _runtime_floors().items():
        actual = observed.get(name)
        assert expected is not None, f"metadata: {name} has no reviewed minimum"
        assert actual is not None, f"{route}: {name} is missing or unbounded"
        assert Version(actual) >= Version(expected), (
            f"{route}: {name}>={actual} weakens the metadata minimum >={expected}"
        )


def test_every_conda_environment_has_a_reviewed_role():
    paths = REPO_ROOT / "devtools/conda-envs"
    actual = {path.name for path in paths.iterdir() if path.suffix in {".yaml", ".yml"}}
    assert actual == set(RUNTIME_ENVIRONMENTS) | set(BUILD_ONLY_ENVIRONMENTS), (
        "Classify new environments before claiming their dependency contract."
    )


@pytest.mark.parametrize("route", RUNTIME_ENVIRONMENTS)
def test_runtime_environments_preserve_required_provider_floors(route):
    _assert_environment_floors(_environment_requirements(route), route)


@pytest.mark.parametrize("provider", ("smonitor", "depdigest"))
@pytest.mark.parametrize("mutation", ("missing", "unbounded", "stale"))
def test_environment_guard_rejects_missing_or_weaker_provider(provider, mutation):
    requirements = [
        item
        for item in _environment_requirements("test_env_core.yaml")
        if _requirement_name(item) != provider
    ]
    if mutation == "unbounded":
        requirements.append(provider)
    elif mutation == "stale":
        requirements.append(f"{provider} >=0.0.0")
    with pytest.raises(AssertionError, match=provider):
        _assert_environment_floors(requirements, "mutated runtime environment")


def test_environment_guard_accepts_stricter_provider_floors():
    requirements = [f"{name} >=99.0.0" for name in _runtime_floors()]
    _assert_environment_floors(requirements, "reviewed stricter environment")


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
    assert _expected_requires_python() == ">=3.11,<3.15"


def test_pyproject_declares_the_supported_python_range():
    assert _pyproject()["project"]["requires-python"] == _expected_requires_python()


def test_full_matrix_tests_every_supported_python_on_every_platform():
    """The full matrix is what makes the declared range true rather than aspirational."""

    text = _read(".github/workflows/CI_full_matrix.yaml")
    cells = set(
        re.findall(r"os:\s*([\w.-]+)\s*,\s*python-version:\s*\"([\d.]+)\"", text)
    )

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


def test_conda_recipe_is_one_python_noarch_artifact():
    text = _read(".github/workflows/build_and_upload_conda_packages.yaml")
    recipe = _read("devtools/conda-build/meta.yaml")
    assert "noarch: python" in recipe
    assert "matrix:" not in text
    assert "python-version: [" not in text


def test_readme_badge_lists_the_supported_pythons():
    badge = "%20%7C%20".join(SUPPORTED_PYTHON)

    assert f"Python-{badge}-" in _read("README.md")


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
            f"pyunitwizard is unbounded in the {extra!r} extra"
        )

    assert (
        _declared_floors(extras["pyunitwizard"])["pyunitwizard"]
        == _declared_floors(extras["all"])["pyunitwizard"]
    ), "the pyunitwizard extra and the all extra declare different floors"


def test_conda_recipe_matches_the_hard_runtime_dependency_set():
    """The recipe and `pyproject.toml` are two statements of one contract.

    Compared in both directions, and against each other rather than against a literal:
    a floor raised in one manifest and not the other is the defect, and a floor raised
    in both is an ordinary change that must not turn this red.
    """

    text = _read("devtools/conda-build/meta.yaml")
    run_block = re.search(r"(?m)^  run:\n(?P<body>(?:    - .*\n)+)", text)
    assert run_block is not None, "the conda recipe has no requirements.run block"

    recipe = _declared_floors(
        [
            line.strip()[2:]
            for line in run_block.group("body").splitlines()
            if line.strip().startswith("- ")
        ]
    )
    recipe.pop("python", None)

    assert recipe == _runtime_floors(), (
        "the conda recipe and pyproject.toml declare different runtime dependencies "
        f"or floors: recipe={recipe}, pyproject={_runtime_floors()}"
    )

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
            f"the manifests declare {floor!r}"
        )

    extras = _pyproject()["project"]["optional-dependencies"]
    assert (
        documented.get("pyunitwizard")
        == _declared_floors(extras["pyunitwizard"])["pyunitwizard"]
    )


def test_docs_compatibility_matrix_states_the_python_range_and_platforms():
    text = _read("docs/content/developer/compatibility-matrix.md")

    assert _expected_requires_python() in text
    for version in SUPPORTED_PYTHON:
        assert re.search(
            rf"\|\s*`{re.escape(version)}`\s*\|\s*required\s*\|\s*required\s*\|\s*required\s*\|",
            text,
        ), f"the matrix page does not require {version} on all platforms"
