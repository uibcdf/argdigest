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


def build_call(
    sig: inspect.Signature,
    arguments: dict[str, Any],
) -> tuple[list[Any], dict[str, Any]]:
    """Rebuild the call shape from the flat mapping `bind_arguments` produced.

    Digestion works on a flat `name -> value` mapping, which is what makes a digester
    reachable by argument name. Calling the function back with `**mapping` would undo
    that flatness at the worst moment: a var-positional parameter has no keyword form
    at all, and a positional-only one refuses to be named. Both would arrive wrong, or
    not arrive. Reconstructing the split here keeps digestion flat without making the
    shape of the call a casualty of it.

    A var-positional parameter is bound as a single tuple and is *unpacked* here, so
    `*items` receives its operands as operands rather than one keyword carrying a tuple.
    """

    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    consumed: set[str] = set()

    parameters = list(sig.parameters.values())
    var_positional = next(
        (p.name for p in parameters if p.kind is inspect.Parameter.VAR_POSITIONAL), None)
    # A non-empty `*rest` forces every parameter before it to travel positionally: there
    # is no way to pass a later positional value while naming an earlier one. When it is
    # empty, the earlier parameters stay keywords, which keeps the common call unchanged.
    positional_required = bool(var_positional and arguments.get(var_positional))
    # A parameter missing from the mapping opens a gap no later value can be passed
    # across, so positional filling stops there. Such a call was already going to fail
    # for want of a required argument, and it now fails the same way.
    positional_open = True

    for parameter in parameters:
        name = parameter.name
        if parameter.kind is inspect.Parameter.VAR_KEYWORD:
            continue
        if name not in arguments:
            positional_open = False
            continue
        value = arguments[name]
        consumed.add(name)
        if positional_open and parameter.kind is inspect.Parameter.VAR_POSITIONAL:
            args.extend(value)
            continue
        if positional_open and (
                parameter.kind is inspect.Parameter.POSITIONAL_ONLY
                or (parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
                    and positional_required)):
            args.append(value)
            continue
        # Either the parameter has a keyword form, or the gap above left no way to pass
        # it positionally. Naming it then raises — but it raises about the argument that
        # is actually missing, which beats dropping these values in silence.
        kwargs[name] = value

    # Whatever the signature does not declare is carried through untouched, exactly as
    # `fn(**bound)` did: an open signature is entitled to it, and a closed one never
    # reaches here with extras because `bind_arguments` already set them aside.
    for name, value in arguments.items():
        if name not in consumed and name not in kwargs:
            kwargs[name] = value

    return args, kwargs
