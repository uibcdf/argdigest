from __future__ import annotations

from typing import Iterable


def normalize_caller(caller, fallback: str | None = None) -> str | None:
    """Returning a normalized caller string or a fallback."""

    if isinstance(caller, str):
        caller = caller.strip()
        return caller or fallback

    if callable(caller):
        module = getattr(caller, "__module__", None)
        name = getattr(caller, "__name__", None)
        if module and name:
            return f"{module}.{name}"
        if name:
            return name

    return fallback


def caller_matches(caller, *suffixes: str) -> bool:
    """Returning whether the normalized caller ends with any suffix."""

    normalized = normalize_caller(caller)
    if not normalized:
        return False
    return any(normalized.endswith(suffix) for suffix in suffixes)


def caller_is_one_of(caller, values: Iterable[str]) -> bool:
    """Returning whether the normalized caller equals any provided value."""

    normalized = normalize_caller(caller)
    if not normalized:
        return False
    return normalized in set(values)
