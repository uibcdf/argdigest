from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITATION = ROOT / "CITATION.cff"


def _scalar(text: str, key: str) -> str:
    match = re.search(
        rf"^{re.escape(key)}:\s*[\"']?([^\n\"']+)[\"']?\s*$", text, re.MULTILINE
    )
    assert match is not None, f"CITATION.cff has no top-level {key!r} field"
    return match.group(1).strip()


def test_citation_metadata_identifies_argdigest() -> None:
    text = CITATION.read_text(encoding="utf-8")

    assert _scalar(text, "cff-version") == "1.2.0"
    assert _scalar(text, "title") == "ArgDigest"
    assert _scalar(text, "type") == "software"
    assert _scalar(text, "url") == "https://github.com/uibcdf/argdigest"
    assert _scalar(text, "repository-code") == "https://github.com/uibcdf/argdigest"
    assert _scalar(text, "license") == "MIT"
    assert not re.search(r"^doi:", text, re.MULTILINE)

    assert "https://orcid.org/0000-0003-3375-870X" in text
    assert "https://orcid.org/0000-0003-2812-1499" in text


def test_citation_version_matches_the_committed_release_plan() -> None:
    plan = tomllib.loads(
        (ROOT / "devtools/conda-build/release_plan.toml").read_text(encoding="utf-8")
    )
    text = CITATION.read_text(encoding="utf-8")
    assert _scalar(text, "version") == plan["version"]

    # A pre-tag candidate is expected to be newer than the latest public tag.
    # After publication the same test accepts equality with the new tag.
    completed = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    if completed.returncode != 0:
        return  # Source archives and shallow CI checkouts may not contain Git tags.

    latest = completed.stdout.strip()
    planned = plan["version"]
    assert all(re.fullmatch(r"\d+\.\d+\.\d+", item) for item in (latest, planned))
    assert tuple(map(int, planned.split("."))) >= tuple(map(int, latest.split(".")))
