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
        # first apply argdigest
        wrapped = digest(kind=kind, rules=rules, map=map)(fn)
        # then enforce typing
        wrapped = beartype(wrapped)
        return wrapped
    return deco
