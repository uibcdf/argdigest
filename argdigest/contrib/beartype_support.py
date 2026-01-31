"""
Optional beartype support.

Usage in a user library:

    from argdigest.contrib.beartype_support import beartype_digest

    @beartype_digest(map={...})
    def fn(...):
        ...
"""

from __future__ import annotations
from typing import Any
from beartype import beartype  # type: ignore
from ..core.decorator import digest


def beartype_digest(*, kind: str | None = None, rules: list[str] | None = None, map: dict[str, dict] | None = None):
    def deco(fn):
        # We want digestion to happen FIRST (outer wrapper), so it transforms values.
        # Then beartype (inner wrapper) checks the transformed values.
        
        # 1. Apply beartype to the original function
        type_checked_fn = beartype(fn)
        
        # 2. Wrap the type-checked function with argdigest
        wrapped = digest(kind=kind, rules=rules, map=map)(type_checked_fn)
        
        return wrapped
    return deco


def _beartype_digest_map(**map_config: dict[str, Any]):
    return beartype_digest(map=map_config)


beartype_digest.map = _beartype_digest_map
