from __future__ import annotations

from functools import wraps
import inspect
import warnings
from importlib import import_module
from typing import Any, Callable

from .registry import Registry
from .context import Context
from .utils import bind_arguments
from .argument_loader import load_argument_digesters, resolve_standardizer
from .argument_registry import ArgumentRegistry
from .config import resolve_config, DigestConfig
from .errors import DigestNotDigestedError, DigestNotDigestedWarning


_UNSET = object()


def digest(
    *,
    kind: str | None = None,
    rules: list[str] | None = None,
    map: dict[str, dict] | None = None,
    digestion_source: str | list[str] | None | object = _UNSET,
    digestion_style: str | object = _UNSET,
    standardizer: Any | object = _UNSET,
    strictness: str | object = _UNSET,
    skip_param: str | object = _UNSET,
    config: DigestConfig | str | None | object = _UNSET,
    **digestion_params: Any,
):
    """
    Main decorator.

    - If `map` is provided, it specifies per-argument configuration:
        @digest(map={"child": {"kind": "feature", "rules": ["feature.base"]}})
    - Otherwise, `kind` and `rules` apply to all arguments (less common).
    """

    def deco(fn: Callable[..., Any]):
        effective_config = config
        if (
            config is _UNSET
            and digestion_source is _UNSET
            and digestion_style is _UNSET
            and standardizer is _UNSET
            and strictness is _UNSET
            and skip_param is _UNSET
        ):
            module_root = fn.__module__.split(".", 1)[0]
            try:
                import_module(f"{module_root}._argdigest")
                effective_config = f"{module_root}._argdigest"
            except Exception:
                effective_config = None

        if effective_config is _UNSET:
            effective_config = None
        cfg = resolve_config(effective_config)
        effective_source = cfg.digestion_source if digestion_source is _UNSET else digestion_source
        effective_style = cfg.digestion_style if digestion_style is _UNSET else digestion_style
        effective_standardizer = cfg.standardizer if standardizer is _UNSET else standardizer
        effective_strictness = cfg.strictness if strictness is _UNSET else strictness
        effective_skip_param = cfg.skip_param if skip_param is _UNSET else skip_param

        standardizer_fn = resolve_standardizer(effective_standardizer)
        digesters_cache: dict[str, Callable[..., Any]] | None = None
        config_map = map or {}
        signature = inspect.signature(fn)
        var_keyword_name = None
        for param in signature.parameters.values():
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                var_keyword_name = param.name
                break

        def get_digesters() -> dict[str, Callable[..., Any]]:
            nonlocal digesters_cache
            if effective_style == "decorator":
                return ArgumentRegistry.get_all()
            if digesters_cache is None:
                digesters_cache = load_argument_digesters(effective_source, effective_style)
            return digesters_cache

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any):
            bound = bind_arguments(fn, *args, **kwargs)

            if bound.get(effective_skip_param, False):
                return fn(**bound)

            caller = f"{fn.__module__}.{fn.__name__}"
            if var_keyword_name and var_keyword_name in bound:
                extra = bound.pop(var_keyword_name) or {}
                if isinstance(extra, dict):
                    bound.update(extra)
            if standardizer_fn is not None:
                bound = standardizer_fn(caller, bound)

            digestion_enabled = True
            if effective_source is None and effective_style == "auto":
                digestion_enabled = bool(ArgumentRegistry.get_all())

            digested: dict[str, Any] = {}
            visiting: set[str] = set()

            def resolve_value_param(sig: inspect.Signature, argname: str) -> str:
                if argname in sig.parameters:
                    return argname
                candidates = [p for p in sig.parameters if p != "caller"]
                if len(candidates) == 1:
                    return candidates[0]
                raise DigestNotDigestedError(
                    f"Cannot determine value parameter for digester '{argname}'",
                )

            def handle_undigested(argname: str) -> None:
                if effective_strictness == "ignore":
                    return
                if effective_strictness == "warn":
                    warnings.warn(
                        f"Argument '{argname}' from '{caller}' has no digester",
                        DigestNotDigestedWarning,
                        stacklevel=2,
                    )
                    return
                if effective_strictness == "error":
                    raise DigestNotDigestedError(
                        f"Argument '{argname}' from '{caller}' has no digester",
                    )
                raise ValueError("strictness must be 'warn', 'error', or 'ignore'")

            def gut(argname: str) -> None:
                if argname in digested:
                    return
                if argname in visiting:
                    raise DigestNotDigestedError(
                        f"Cyclic dependency detected while digesting '{argname}'",
                    )
                visiting.add(argname)

                fn_digest = digesters.get(argname)
                if fn_digest is None:
                    handle_undigested(argname)
                    digested[argname] = bound.get(argname)
                    visiting.remove(argname)
                    return

                sig = inspect.signature(fn_digest)
                value_param = resolve_value_param(sig, argname)
                kwargs_for_digest: dict[str, Any] = {}
                for param_name in sig.parameters:
                    if param_name == value_param:
                        kwargs_for_digest[param_name] = bound.get(argname)
                    elif param_name == "caller":
                        kwargs_for_digest[param_name] = caller
                    elif param_name in bound:
                        gut(param_name)
                        kwargs_for_digest[param_name] = digested[param_name]
                    elif param_name in digestion_params:
                        kwargs_for_digest[param_name] = digestion_params[param_name]
                    else:
                        kwargs_for_digest[param_name] = None

                digested[argname] = fn_digest(**kwargs_for_digest)
                visiting.remove(argname)

            if digestion_enabled:
                digesters = get_digesters()
                for argname in bound:
                    if argname == "self":
                        continue
                    gut(argname)

                # update bound with digested values for downstream pipelines
                bound = {**bound, **digested}

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
