from __future__ import annotations

from functools import wraps
import inspect
import threading
import warnings
from typing import Any, Callable

from .registry import Registry
from .context import Context
from .utils import bind_arguments
from .argument_loader import load_argument_digesters, resolve_standardizer
from .argument_registry import ArgumentRegistry
from .config import resolve_config, DigestConfig, get_env_config_module
from .errors import DigestNotDigestedError, DigestNotDigestedWarning
from .logger import get_logger
from smonitor import signal
from depdigest import dep_digest

from dataclasses import dataclass, field
from .contract import ValidatedPayload

_UNSET = object()
logger = get_logger()

# Global cache for digester metadata to avoid redundant inspect.signature calls
# (fn_dig, argname) -> (sig, value_param)
_DIGESTER_METADATA_CACHE: dict[tuple[Callable, str], tuple[inspect.Signature, str]] = {}
_DIGESTER_METADATA_LOCK = threading.RLock()


def _normalize_strictness(strictness: str) -> str:
    value = strictness.lower()
    if value in ("error", "raise"):
        return "error"
    if value in ("warn", "warning"):
        return "warn"
    if value in ("ignore", "silent", "none"):
        return "ignore"
    raise ValueError("strictness must be one of: error/raise, warn/warning, ignore/silent/none")

def _resolve_value_param(sig: inspect.Signature, argname: str) -> str:
    if argname in sig.parameters:
        return argname
    candidates = [p for p in sig.parameters if p != "caller"]
    if len(candidates) == 1:
        return candidates[0]
    raise DigestNotDigestedError(
        f"Cannot determine value parameter for digester '{argname}'",
    )

def get_digester_metadata(fn_dig: Callable, argname: str) -> tuple[inspect.Signature, str]:
    key = (fn_dig, argname)
    with _DIGESTER_METADATA_LOCK:
        if key not in _DIGESTER_METADATA_CACHE:
            sig_dig = inspect.signature(fn_dig)
            value_param = _resolve_value_param(sig_dig, argname)
            _DIGESTER_METADATA_CACHE[key] = (sig_dig, value_param)
        return _DIGESTER_METADATA_CACHE[key]


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
    enable_argument_digestion: bool = True
    profiling: bool = False
    var_keyword_name: str | None = None


def arg_digest(
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
    @dep_digest('beartype', when={'type_check': True})
    def deco(fn: Callable[..., Any]):
        fn_to_wrap = fn
        if type_check:
            try:
                from beartype import beartype
                fn_to_wrap = beartype(fn)
            except ImportError:
                try:
                    from smonitor.integrations import emit_from_catalog, merge_extra
                    from .._private.smonitor import CATALOG, PACKAGE_ROOT, META

                    emit_from_catalog(
                        CATALOG["warnings"]["TypeCheckSkippedWarning"],
                        package_root=PACKAGE_ROOT,
                        extra=merge_extra(META, {"caller": f"{fn.__module__}.{fn.__name__}"}),
                    )
                except Exception as exc:
                    warnings.warn(
                        (
                            "type_check=True but 'beartype' is not installed. "
                            f"Skipping in {fn.__module__}.{fn.__name__}. "
                            f"SMonitor emission failed with: {exc!r}"
                        ),
                        RuntimeWarning,
                    )

        # Resolve effective parameters
        eff_config = config
        auto_module_config = None
        env_module_config = None
        if (eff_config is _UNSET and digestion_source is _UNSET and digestion_style is _UNSET):
            module_root = fn.__module__.split(".", 1)[0]
            auto_module_config = f"{module_root}._argdigest"
            env_module_config = get_env_config_module()
            eff_config = env_module_config or auto_module_config

        try:
            cfg = resolve_config(None if eff_config is _UNSET else eff_config)
        except (ImportError, ModuleNotFoundError):
            # If env config is set but unavailable, fall back to auto module config.
            if env_module_config and auto_module_config:
                try:
                    cfg = resolve_config(auto_module_config)
                except (ImportError, ModuleNotFoundError):
                    cfg = resolve_config(None)
            else:
                cfg = resolve_config(None)
        
        eff_source = cfg.digestion_source if digestion_source is _UNSET else digestion_source
        eff_style = cfg.digestion_style if digestion_style is _UNSET else digestion_style
        eff_standardizer = cfg.standardizer if standardizer is _UNSET else standardizer
        eff_strictness = _normalize_strictness(cfg.strictness if strictness is _UNSET else strictness)
        eff_skip_param = cfg.skip_param if skip_param is _UNSET else skip_param
        eff_profiling = cfg.profiling if profiling is _UNSET else profiling
        
        effective_puw_context = {**(cfg.puw_context or {}), **(puw_context or {})}

        # Pre-load digesters
        if eff_style == "decorator":
            available_digesters = ArgumentRegistry.get_all()
        else:
            available_digesters = load_argument_digesters(eff_source, eff_style)

        # Default behavior for pure pipeline usage:
        # when users do not configure argument-centric digestion and no digesters are discovered,
        # skip argument digestion pass to avoid non-actionable warnings.
        explicit_argdigestion_config = any(
            x is not _UNSET
            for x in (digestion_source, digestion_style, standardizer, strictness, config)
        )
        enable_argument_digestion = not (
            not explicit_argdigestion_config
            and eff_style == "auto"
            and eff_source is None
            and not available_digesters
            and eff_standardizer is None
        )

        # Inspect signature once
        signature = inspect.signature(fn)
        var_keyword_name = next((p.name for p in signature.parameters.values() if p.kind == inspect.Parameter.VAR_KEYWORD), None)

        # Build pipeline targets
        pipeline_targets = map or {}
        if kind is not None:
            for p in signature.parameters.values():
                if p.name != "self" and p.kind not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
                    if p.name not in pipeline_targets:
                        pipeline_targets[p.name] = {"kind": kind, "rules": rules or []}

        plan = DigestionPlan(
            digesters=available_digesters,
            pipeline_targets=pipeline_targets,
            strictness=eff_strictness,
            skip_param=eff_skip_param,
            standardizer=resolve_standardizer(eff_standardizer),
            enable_argument_digestion=enable_argument_digestion,
            profiling=bool(eff_profiling),
            var_keyword_name=var_keyword_name
        )

        @wraps(fn)
        @signal(tags=["digestion"], exception_level="DEBUG")
        def wrapper(*args: Any, **kwargs: Any):
            logger.debug(f"Digesting arguments for {fn.__name__}")
            if plan.profiling:
                wrapper.audit_log = []

            def _run_digestion():
                bound = bind_arguments(fn, *args, **kwargs)
                if bound.get(plan.skip_param, False):
                    return fn_to_wrap(**bound)

                caller = f"{fn.__module__}.{fn.__name__}"
                if plan.var_keyword_name and plan.var_keyword_name in bound:
                    extra = bound.pop(plan.var_keyword_name) or {}
                    if isinstance(extra, dict):
                        bound.update(extra)
                
                if plan.standardizer:
                    bound = plan.standardizer(caller, bound)

                digested: dict[str, Any] = {}
                visiting_path: list[str] = []

                def gut(argname: str) -> None:
                    if argname in digested:
                        return
                    if argname in visiting_path:
                        ctx_error = Context(function_name=fn.__name__, argname=argname, value=bound.get(argname), all_args=bound)
                        raise DigestNotDigestedError(f"Cycle: {' -> '.join(visiting_path + [argname])}", context=ctx_error)
                    visiting_path.append(argname)

                    # --- Passport Protocol: Check for ValidatedPayload ---
                    val = bound.get(argname)
                    if isinstance(val, ValidatedPayload):
                        digested[argname] = val.value
                        visiting_path.pop()
                        return
                    # ---------------------------------------------------

                    fn_digest = plan.digesters.get(argname)
                    if fn_digest is None:
                        ctx_error = Context(function_name=fn.__name__, argname=argname, value=bound.get(argname), all_args=bound)
                        if plan.strictness == "error": 
                            raise DigestNotDigestedError(f"No digester for {argname}", context=ctx_error)
                        if plan.strictness == "warn":
                            # Always issue standard Python warning for testing/simple setups
                            warnings.warn(
                                DigestNotDigestedWarning(
                                    message=f"No digester for {argname}",
                                    context=ctx_error,
                                )
                            )
                        digested[argname] = bound.get(argname)
                        visiting_path.pop()
                        return

                    # Fetch metadata ON DEMAND (Cached)
                    sig, value_param = get_digester_metadata(fn_digest, argname)
                    
                    kwargs_for_digest = {}
                    for p_name in sig.parameters:
                        if p_name == value_param:
                            kwargs_for_digest[p_name] = bound.get(argname)
                        elif p_name == "caller":
                            kwargs_for_digest[p_name] = caller
                        elif p_name in bound:
                            gut(p_name)
                            kwargs_for_digest[p_name] = digested[p_name]
                        elif p_name in digestion_params:
                            kwargs_for_digest[p_name] = digestion_params[p_name]
                        else:
                            kwargs_for_digest[p_name] = None

                    try:
                        digested[argname] = fn_digest(**kwargs_for_digest)
                    except Exception as e:
                        # Centralized observability: report to smonitor
                        try:
                            from smonitor import emit
                            emit("DEBUG", f"Digestion failed for argument '{argname}'", 
                                 extra={
                                     "code": "MSM-DBG-PROBE-001",
                                     "argname": argname,
                                     "caller": caller,
                                     "cause_exception": type(e).__name__,
                                     "cause_message": str(e)
                                 })
                        except:
                            pass
                        # Re-raise with cause attached
                        if hasattr(e, 'message'): # Some custom errors might have message
                             raise e
                        raise e

                    visiting_path.pop()

                if plan.enable_argument_digestion:
                    for argname in bound:
                        if argname != "self":
                            gut(argname)
                    bound.update(digested)
                for argname, cfg_pipe in plan.pipeline_targets.items():
                    if argname not in bound:
                        continue
                    # Pass the wrapper's audit_log to the context
                    audit_log = getattr(wrapper, "audit_log", None)
                    ctx = Context(
                        function_name=fn.__name__, 
                        argname=argname, 
                        value=bound[argname], 
                        all_args=bound,
                        audit_log=audit_log,
                        _profiling=plan.profiling
                    )
                    # Use the kind and rules from the specific target config
                    eff_kind = cfg_pipe.get("kind")
                    eff_rules = cfg_pipe.get("rules")
                    try:
                        bound[argname] = Registry.run(eff_kind, eff_rules, bound[argname], ctx)
                    except Exception as e:
                        try:
                            from smonitor import emit
                            emit("DEBUG", f"Pipeline failed for argument '{argname}'", 
                                 extra={
                                     "code": "MSM-DBG-PROBE-001",
                                     "argname": argname,
                                     "pipeline": f"{eff_kind}.{eff_rules}",
                                     "cause_exception": type(e).__name__,
                                     "cause_message": str(e)
                                 })
                        except:
                            pass
                        raise e

                return fn_to_wrap(**bound)

            if effective_puw_context:
                from ..contrib.pyunitwizard_support import context as puw_ctx_manager
                with puw_ctx_manager(**effective_puw_context):
                    return _run_digestion()
            return _run_digestion()

        wrapper.digestion_plan = plan
        wrapper.audit_log = [] if plan.profiling else None
        return wrapper
    return deco

def _arg_digest_map(
    type_check=False,
    puw_context=None,
    profiling=_UNSET,
    config=_UNSET,
    **map_config
):
    return arg_digest(map=map_config, type_check=type_check, puw_context=puw_context, profiling=profiling, config=config)

arg_digest.map = _arg_digest_map
