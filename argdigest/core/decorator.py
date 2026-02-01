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
from .logger import get_logger


_UNSET = object()
logger = get_logger()


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
    type_check: bool = False,
    puw_context: dict[str, Any] | None = None,
    profiling: bool | object = _UNSET,
    **digestion_params: Any,
):
    """
    Main decorator.

    - type_check: If True, uses beartype to enforce type hints on the *digested* values.
    - puw_context: Optional PyUnitWizard context configuration (e.g. {'form': 'pint'}).
    - profiling: If True, collects performance metrics for each pipeline step.
    """

    def deco(fn: Callable[..., Any]):
        # Apply beartype first (so it becomes the inner wrapper)
        # Sequence: digest_wrapper -> beartype_wrapper -> original_fn
        fn_to_wrap = fn
        if type_check:
            try:
                from beartype import beartype
                fn_to_wrap = beartype(fn)
            except ImportError:
                warnings.warn(
                    "type_check=True requested but 'beartype' is not installed. Skipping type checking.",
                    RuntimeWarning
                )

        effective_config = config
        if (
            config is _UNSET
            and digestion_source is _UNSET
            and digestion_style is _UNSET
            and standardizer is _UNSET
            and strictness is _UNSET
            and skip_param is _UNSET
            and puw_context is None
            and profiling is _UNSET
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
        effective_profiling = cfg.profiling if profiling is _UNSET else profiling
        
        # Merge puw_context: kwargs take precedence over config
        base_puw_ctx = cfg.puw_context or {}
        override_puw_ctx = puw_context if puw_context is not None else {}
        effective_puw_context = {**base_puw_ctx, **override_puw_ctx}

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
            
            def _run_digestion():
                bound = bind_arguments(fn, *args, **kwargs)

                if bound.get(effective_skip_param, False):
                    return fn_to_wrap(**bound)

                caller = f"{fn.__module__}.{fn.__name__}"
                logger.debug(f"Digesting arguments for {caller}")

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
                visiting_path: list[str] = []

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

                    # Create a lightweight context for the error
                    from types import SimpleNamespace
                    error_ctx = SimpleNamespace(
                        function_name=caller,
                        argname=argname,
                        value=bound.get(argname),
                        all_args=bound
                    )

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
                            context=error_ctx,
                            hint="Check if the argument name is correct or if a digester is registered."
                        )
                    raise ValueError("strictness must be 'warn', 'error', or 'ignore'")

                def gut(argname: str) -> None:
                    if argname in digested:
                        return
                    if argname in visiting_path:
                        path = " -> ".join(visiting_path + [argname])
                        raise DigestNotDigestedError(
                            f"Cyclic dependency detected: {path}",
                        )
                    visiting_path.append(argname)

                    fn_digest = digesters.get(argname)
                    if fn_digest is None:
                        handle_undigested(argname)
                        digested[argname] = bound.get(argname)
                        visiting_path.pop()
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
                    visiting_path.pop()

                if digestion_enabled:
                    digesters = get_digesters()
                    for argname in bound:
                        if argname == "self":
                            continue
                        gut(argname)

                    # update bound with digested values for downstream pipelines
                    bound = {**bound, **digested}

                # process each argument that appears in config_map
                # if map is None, apply kind and rules to all arguments
                if map is None:
                    targets = {argname: {"kind": kind, "rules": rules or []} for argname in bound if argname != "self"}
                else:
                    targets = config_map

                all_audit_logs = []

                for argname, cfg in targets.items():
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
                    # Pass profiling flag via private attribute in ctx for Registry.run
                    if effective_profiling:
                        setattr(ctx, "_profiling", True)

                    # run pipelines: they may transform the value
                    new_val = Registry.run(arg_kind, arg_rules, arg_val, ctx)
                    bound[argname] = new_val
                    
                    if effective_profiling:
                        all_audit_logs.extend(ctx.audit_log)

                if effective_profiling:
                    # Store audit log in function metadata or log it?
                    # For now, let's attach it to the function object for inspection if possible, 
                    # but since it's a wrapper, we attach it to the wrapper? 
                    # Better: define a mechanism to retrieve it.
                    # For now, let's just log it at debug level.
                    logger.debug(f"Audit log for {caller}: {all_audit_logs}")
                    # And attach to wrapper for testing/inspection
                    wrapper.audit_log = all_audit_logs

                logger.debug(f"Digestion complete for {caller}")
                # call original (or beartype-wrapped) with possibly updated args
                return fn_to_wrap(**bound)

            # Execution with optional PUW context
            if effective_puw_context:
                from ..contrib.pyunitwizard_support import context as puw_ctx_manager
                with puw_ctx_manager(**effective_puw_context):
                    return _run_digestion()
            else:
                return _run_digestion()

        return wrapper

    return deco


def _digest_map(
    type_check: bool = False,
    puw_context: dict[str, Any] | None = None,
    profiling: bool | object = _UNSET,
    **map_config: dict[str, Any]
):
    return digest(map=map_config, type_check=type_check, puw_context=puw_context, profiling=profiling)


digest.map = _digest_map