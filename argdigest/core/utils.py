from __future__ import annotations
import inspect
from typing import Any, Callable


def bind_arguments(
    fn: Callable[..., Any],
    *args: Any,
    sig: inspect.Signature | None = None,
    var_keyword_name: str | None = None,
    extras_out: dict[str, Any] | None = None,
    **kwargs: Any
) -> dict[str, Any]:
    """Bind a call to a signature, setting aside what the signature cannot take.

    A closed signature cannot be called with a keyword it does not declare, so those
    keywords are held back here. They are *set aside*, not judged: pass `extras_out` to
    receive them, so the function-contract stage can decide whether they are a typo, a
    legitimate open-domain keyword, or something to tolerate. Deciding that here would
    put a policy in a binding step, and would make the decision invisible to the layer
    designed to take it.
    """

    if sig is None:
        sig = inspect.signature(fn)
        # Check if the function accepts **kwargs
        var_keyword_name = next((p.name for p in sig.parameters.values() if p.kind == p.VAR_KEYWORD), None)

    if not var_keyword_name:
        valid_params = set(sig.parameters.keys())
        if extras_out is not None:
            extras_out.update({k: v for k, v in kwargs.items() if k not in valid_params})
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
