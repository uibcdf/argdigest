from __future__ import annotations

from pathlib import Path

import argdigest


def _extract_autosummary_items(api_index: str) -> list[str]:
    lines = api_index.splitlines()
    inside = False
    items: list[str] = []

    for line in lines:
        if ".. autosummary::" in line:
            inside = True
            continue
        if not inside:
            continue
        if line.strip() == "```":
            break
        stripped = line.strip()
        if not stripped or stripped.startswith(":") or stripped.startswith(".."):
            continue
        items.append(stripped)

    return items


def test_api_reference_matches_public_exports():
    api_index = Path("docs/api/index.md").read_text(encoding="utf-8")
    documented = _extract_autosummary_items(api_index)
    assert documented == list(argdigest.__all__)
