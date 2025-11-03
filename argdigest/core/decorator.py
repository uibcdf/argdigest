from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from .registry import Registry
from .context import Context
from .utils import bind_arguments


def digest(*, kind: str | None = None, rules: list[str] | None = None, map: dict[str, dict] | None = None):
    """
    Main decorator.

    - If `map` is provided, it specifies per-argument configuration:
        @digest(map={"child": {"kind": "feature", "rules": ["feature.base"]}})
    - Otherwise, `kind` and `rules` apply to all arguments (less common).
    """

    def deco(fn: Callable[..., Any]):
        config_map = map or {}

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any):
            bound = bind_arguments(fn, *args, **kwargs)

            # process each argument that appears in config_map
            for argname, cfg in config_map.items():
                if argname not in bound:
                    continue
                arg_val = bound[argname]
                arg_kind = cfg.get("kind", kind)
                arg_rules = cfg.get("rules", rules or [])
                if arg_kind is None:
                    continue

                ctx = Context(
                    function_name=fn.__name__,
                    argname=argname,
                    value=arg_val,
                    all_args=bound,
                )
                # run pipelines: they may transform the value
                new_val = Registry.run(arg_kind, arg_rules, arg_val, ctx)
                bound[argname] = new_val

            # call original with possibly updated args
            return fn(**bound)

        return wrapper

    return deco

