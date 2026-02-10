from __future__ import annotations
from inspect import signature
from typing import Any, Callable


def bind_arguments(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> dict[str, Any]:
    sig = signature(fn)
    
    # Check if the function accepts **kwargs
    has_varkw = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
    
    if not has_varkw:
        # Filter kwargs to only include valid parameters
        valid_params = set(sig.parameters.keys())
        kwargs = {k: v for k, v in kwargs.items() if k in valid_params}

    bound = sig.bind_partial(*args, **kwargs)
    bound.apply_defaults()
    return dict(bound.arguments)
