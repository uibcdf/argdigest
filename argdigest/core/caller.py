from __future__ import annotations

import keyword
from typing import Any, Callable, Iterable


def validate_contract_owner(owner: str | None) -> str | None:
    """Validate None, definition mode, or an exact dotted caller key.

    The key is declaration data: it is neither imported nor inferred from a class.
    Reject patterns and whitespace rather than silently selecting another contract.
    """
    if owner is None:
        return None
    if not isinstance(owner, str):
        raise TypeError(
            "contract_owner must be None, 'definition' or an exact dotted caller key"
        )
    if owner == "definition":
        return owner
    parts = owner.split(".")
    if len(parts) < 2 or any(
        not part.isidentifier() or keyword.iskeyword(part) for part in parts
    ):
        raise ValueError("contract_owner must be an exact dotted caller key")
    return owner


def resolve_contract_owner(fn: Callable[..., Any], owner: str | None) -> str | None:
    """Resolve declaration-time contract identity; None leaves runtime lookup active.

    Definition mode uses the existing module.function caller convention. Exact
    keys permit a logical owner different from the implementation module.
    """
    owner = validate_contract_owner(owner)
    if owner == "definition":
        module, name = getattr(fn, "__module__", None), getattr(fn, "__name__", None)
        if not callable(fn) or not isinstance(module, str) or not isinstance(name, str):
            raise TypeError("definition contract_owner requires a named callable")
        return validate_contract_owner(f"{module}.{name}")
    return owner


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


def caller_startswith(caller, *prefixes: str) -> bool:
    """Returning whether the normalized caller starts with any prefix."""

    normalized = normalize_caller(caller)
    if not normalized:
        return False
    return any(normalized.startswith(prefix) for prefix in prefixes)
