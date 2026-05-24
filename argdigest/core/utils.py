from __future__ import annotations
import inspect
from typing import Any, Callable


def bind_arguments(
    fn: Callable[..., Any],
    *args: Any,
    sig: inspect.Signature | None = None,
    var_keyword_name: str | None = None,
    **kwargs: Any
) -> dict[str, Any]:
    if sig is None:
        sig = inspect.signature(fn)
        # Check if the function accepts **kwargs
        var_keyword_name = next((p.name for p in sig.parameters.values() if p.kind == p.VAR_KEYWORD), None)
    
    if not var_keyword_name:
        # Filter kwargs to only include valid parameters
        valid_params = set(sig.parameters.keys())
        kwargs = {k: v for k, v in kwargs.items() if k in valid_params}

    bound = sig.bind_partial(*args, **kwargs)
    bound.apply_defaults()
    
    arguments = dict(bound.arguments)
    
    # Flatten var_keyword arguments if present
    if var_keyword_name and var_keyword_name in arguments:
        extra = arguments.pop(var_keyword_name)
        if isinstance(extra, dict):
            arguments.update(extra)
            
    return arguments
