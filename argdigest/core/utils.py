from __future__ import annotations
from inspect import signature
from typing import Any, Callable


def bind_arguments(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> dict[str, Any]:
    sig = signature(fn)
    bound = sig.bind_partial(*args, **kwargs)
    bound.apply_defaults()
    return dict(bound.arguments)
