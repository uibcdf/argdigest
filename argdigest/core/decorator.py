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


from dataclasses import dataclass, field

_UNSET = object()
logger = get_logger()


@dataclass
class DigestionPlan:
    """Stores pre-calculated digestion logic for a specific function."""
    digesters: dict[str, Callable[..., Any]] = field(default_factory=dict)
    # Target arguments for pipelines: argname -> {kind, rules}
    pipeline_targets: dict[str, dict[str, Any]] = field(default_factory=dict)
    # Metadata for the plan
    strictness: str = "warn"
    skip_param: str = "skip_digestion"
    standardizer: Callable[[str, dict], dict] | None = None
    profiling: bool = False
    var_keyword_name: str | None = None
    
    # Pre-calculated signature and parameter details
    digester_signatures: dict[str, inspect.Signature] = field(default_factory=dict)
    digester_value_params: dict[str, str] = field(default_factory=dict)


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
        
        # Resolve effective parameters
        eff_source = cfg.digestion_source if digestion_source is _UNSET else digestion_source
        eff_style = cfg.digestion_style if digestion_style is _UNSET else digestion_style
        eff_standardizer = cfg.standardizer if standardizer is _UNSET else standardizer
        eff_strictness = cfg.strictness if strictness is _UNSET else strictness
        eff_skip_param = cfg.skip_param if skip_param is _UNSET else skip_param
        eff_profiling = cfg.profiling if profiling is _UNSET else profiling
        
        # Merge puw_context
        base_puw_ctx = cfg.puw_context or {}
        override_puw_ctx = puw_context if puw_context is not None else {}
        effective_puw_context = {**base_puw_ctx, **override_puw_ctx}

        # Pre-load digesters
        if eff_style == "decorator":
            available_digesters = ArgumentRegistry.get_all()
        else:
            available_digesters = load_argument_digesters(eff_source, eff_style)

        # Inspect function signature once
        signature = inspect.signature(fn)
        var_keyword_name = None
        for param in signature.parameters.values():
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                var_keyword_name = param.name
                break

        # Build pipeline targets map
        config_map = map or {}
        if map is None and kind is not None:
            # If kind is provided globally, it applies to all parameters except 'self'
            pipeline_targets = {
                p.name: {"kind": kind, "rules": rules or []} 
                for p in signature.parameters.values() 
                if p.name != "self" and p.kind != inspect.Parameter.VAR_KEYWORD and p.kind != inspect.Parameter.VAR_POSITIONAL
            }
        else:
            pipeline_targets = config_map

        # Helper to resolve value parameter name for a digester
        def _resolve_value_param(sig: inspect.Signature, argname: str) -> str:
            if argname in sig.parameters:
                return argname
            candidates = [p for p in sig.parameters if p != "caller"]
            if len(candidates) == 1:
                return candidates[0]
            raise DigestNotDigestedError(
                f"Cannot determine value parameter for digester '{argname}'",
            )

        # Pre-calculate digester metadata
        digester_signatures = {}
        digester_value_params = {}
        for argname, fn_dig in available_digesters.items():
            sig_dig = inspect.signature(fn_dig)
            digester_signatures[argname] = sig_dig
            digester_value_params[argname] = _resolve_value_param(sig_dig, argname)

        # Create the final Plan
        plan = DigestionPlan(
            digesters=available_digesters,
            pipeline_targets=pipeline_targets,
            strictness=eff_strictness,
            skip_param=eff_skip_param,
            standardizer=resolve_standardizer(eff_standardizer),
            profiling=bool(eff_profiling),
            var_keyword_name=var_keyword_name,
            digester_signatures=digester_signatures,
            digester_value_params=digester_value_params
        )

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any):
            
            def _run_digestion():
                bound = bind_arguments(fn, *args, **kwargs)

                if bound.get(plan.skip_param, False):
                    return fn_to_wrap(**bound)

                caller = f"{fn.__module__}.{fn.__name__}"
                logger.debug(f"Digesting arguments for {caller}")

                if plan.var_keyword_name and plan.var_keyword_name in bound:
                    extra = bound.pop(plan.var_keyword_name) or {}
                    if isinstance(extra, dict):
                        bound.update(extra)
                
                if plan.standardizer is not None:
                    bound = plan.standardizer(caller, bound)

                digested: dict[str, Any] = {}
                visiting_path: list[str] = []

                def handle_undigested(argname: str) -> None:
                    if plan.strictness == "ignore":
                        return
                    
                    from types import SimpleNamespace
                    error_ctx = SimpleNamespace(
                        function_name=caller,
                        argname=argname,
                        value=bound.get(argname),
                        all_args=bound
                    )

                    if plan.strictness == "warn":
                        warnings.warn(
                            f"Argument '{argname}' from '{caller}' has no digester",
                            DigestNotDigestedWarning,
                            stacklevel=2,
                        )
                        return
                    if plan.strictness == "error":
                        raise DigestNotDigestedError(
                            f"Argument '{argname}' from '{caller}' has no digester",
                            context=error_ctx,
                            hint="Check if the argument name is correct or if a digester is registered."
                        )

                def gut(argname: str) -> None:
                    if argname in digested:
                        return
                    if argname in visiting_path:
                        path = " -> ".join(visiting_path + [argname])
                        raise DigestNotDigestedError(f"Cyclic dependency detected: {path}")
                    
                    visiting_path.append(argname)

                    fn_digest = plan.digesters.get(argname)
                    if fn_digest is None:
                        handle_undigested(argname)
                        digested[argname] = bound.get(argname)
                        visiting_path.pop()
                        return

                    sig = plan.digester_signatures[argname]
                    value_param = plan.digester_value_params[argname]
                    
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

                # Execute argument-centric digestion
                for argname in bound:
                    if argname == "self":
                        continue
                    gut(argname)

                # Update bound with digested values
                bound.update(digested)

                # Execute pipeline targets
                runtime_targets = plan.pipeline_targets
                # Dynamically add global targets for **kwargs if kind was provided
                if map is None and kind is not None:
                    for argname in bound:
                        if argname not in runtime_targets and argname != "self":
                            # We don't want to modify the static plan, so we use a copy for runtime
                            if runtime_targets is plan.pipeline_targets:
                                runtime_targets = plan.pipeline_targets.copy()
                            runtime_targets[argname] = {"kind": kind, "rules": rules or []}

                all_audit_logs = []

                for argname, cfg_pipe in runtime_targets.items():
                    if argname not in bound:
                        continue
                    
                    arg_val = bound[argname]
                    arg_kind = cfg_pipe.get("kind", kind)
                    arg_rules = cfg_pipe.get("rules", rules or [])
                    if arg_kind is None:
                        continue

                    ctx = Context(
                        function_name=fn.__name__,
                        argname=argname,
                        value=arg_val,
                        all_args=bound,
                    )
                    if plan.profiling:
                        setattr(ctx, "_profiling", True)

                    new_val = Registry.run(arg_kind, arg_rules, arg_val, ctx)
                    bound[argname] = new_val
                    
                    if plan.profiling:
                        all_audit_logs.extend(ctx.audit_log)

                if plan.profiling:
                    logger.debug(f"Audit log for {caller}: {all_audit_logs}")
                    wrapper.audit_log = all_audit_logs

                logger.debug(f"Digestion complete for {caller}")
                return fn_to_wrap(**bound)

            # Execution with optional PUW context
            if effective_puw_context:
                from ..contrib.pyunitwizard_support import context as puw_ctx_manager
                with puw_ctx_manager(**effective_puw_context):
                    return _run_digestion()
            else:
                return _run_digestion()

        # Attach the plan for auditing/inspection
        wrapper.digestion_plan = plan
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