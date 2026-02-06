from __future__ import annotations

from functools import wraps, lru_cache
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

# Global cache for digester metadata to avoid redundant inspect.signature calls
# (fn_dig, argname) -> (sig, value_param)
_DIGESTER_METADATA_CACHE: dict[tuple[Callable, str], tuple[inspect.Signature, str]] = {}

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
    def deco(fn: Callable[..., Any]):
        fn_to_wrap = fn
        if type_check:
            try:
                from beartype import beartype
                fn_to_wrap = beartype(fn)
            except ImportError:
                try:
                    from smonitor.integrations import emit_from_catalog
                    from .._private.smonitor import CATALOG, PACKAGE_ROOT

                    emit_from_catalog(CATALOG["typecheck_skip"], package_root=PACKAGE_ROOT)
                except Exception:
                    warnings.warn("type_check=True but 'beartype' is not installed. Skipping.", RuntimeWarning)

        # Resolve effective parameters
        eff_config = config
        if (eff_config is _UNSET and digestion_source is _UNSET and digestion_style is _UNSET):
            module_root = fn.__module__.split(".", 1)[0]
            eff_config = f"{module_root}._argdigest"
        
        cfg = resolve_config(None if eff_config is _UNSET else eff_config)
        
        eff_source = cfg.digestion_source if digestion_source is _UNSET else digestion_source
        eff_style = cfg.digestion_style if digestion_style is _UNSET else digestion_style
        eff_standardizer = cfg.standardizer if standardizer is _UNSET else standardizer
        eff_strictness = cfg.strictness if strictness is _UNSET else strictness
        eff_skip_param = cfg.skip_param if skip_param is _UNSET else skip_param
        eff_profiling = cfg.profiling if profiling is _UNSET else profiling
        
        effective_puw_context = {**(cfg.puw_context or {}), **(puw_context or {})}

        # Pre-load digesters
        if eff_style == "decorator":
            available_digesters = ArgumentRegistry.get_all()
        else:
            available_digesters = load_argument_digesters(eff_source, eff_style)

        # Inspect signature once
        signature = inspect.signature(fn)
        var_keyword_name = next((p.name for p in signature.parameters.values() if p.kind == inspect.Parameter.VAR_KEYWORD), None)

        # Build pipeline targets
        pipeline_targets = map or {}
        if map is None and kind is not None:
            pipeline_targets = {p.name: {"kind": kind, "rules": rules or []} 
                                for p in signature.parameters.values() 
                                if p.name != "self" and p.kind not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)}

        plan = DigestionPlan(
            digesters=available_digesters,
            pipeline_targets=pipeline_targets,
            strictness=eff_strictness,
            skip_param=eff_skip_param,
            standardizer=resolve_standardizer(eff_standardizer),
            profiling=bool(eff_profiling),
            var_keyword_name=var_keyword_name
        )

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any):
            def _run_digestion():
                bound = bind_arguments(fn, *args, **kwargs)
                if bound.get(plan.skip_param, False):
                    return fn_to_wrap(**bound)

                caller = f"{fn.__module__}.{fn.__name__}"
                if plan.var_keyword_name and plan.var_keyword_name in bound:
                    extra = bound.pop(plan.var_keyword_name) or {}
                    if isinstance(extra, dict): bound.update(extra)
                
                if plan.standardizer: bound = plan.standardizer(caller, bound)

                digested: dict[str, Any] = {}
                visiting_path: list[str] = []

                def gut(argname: str) -> None:
                    if argname in digested: return
                    if argname in visiting_path: raise DigestNotDigestedError(f"Cycle: {' -> '.join(visiting_path + [argname])}")
                    visiting_path.append(argname)

                    fn_digest = plan.digesters.get(argname)
                    if fn_digest is None:
                        if plan.strictness == "error": raise DigestNotDigestedError(f"No digester for {argname}")
                        if plan.strictness == "warn":
                            try:
                                from smonitor.integrations import emit_from_catalog
                                from .._private.smonitor import CATALOG, PACKAGE_ROOT

                                emit_from_catalog(
                                    CATALOG["missing_digester"],
                                    package_root=PACKAGE_ROOT,
                                    extra={"argname": argname},
                                )
                            except Exception:
                                warnings.warn(f"No digester for {argname}")
                        digested[argname] = bound.get(argname)
                        visiting_path.pop(); return

                    # Fetch metadata ON DEMAND (Cached)
                    sig, value_param = get_digester_metadata(fn_digest, argname)
                    
                    kwargs_for_digest = {}
                    for p_name in sig.parameters:
                        if p_name == value_param: kwargs_for_digest[p_name] = bound.get(argname)
                        elif p_name == "caller": kwargs_for_digest[p_name] = caller
                        elif p_name in bound:
                            gut(p_name)
                            kwargs_for_digest[p_name] = digested[p_name]
                        elif p_name in digestion_params: kwargs_for_digest[p_name] = digestion_params[p_name]
                        else: kwargs_for_digest[p_name] = None

                    digested[argname] = fn_digest(**kwargs_for_digest)
                    visiting_path.pop()

                for argname in bound:
                    if argname != "self": gut(argname)

                bound.update(digested)
                for argname, cfg_pipe in plan.pipeline_targets.items():
                    if argname not in bound: continue
                    ctx = Context(function_name=fn.__name__, argname=argname, value=bound[argname], all_args=bound)
                    bound[argname] = Registry.run(cfg_pipe.get("kind", kind), cfg_pipe.get("rules", rules or []), bound[argname], ctx)

                return fn_to_wrap(**bound)

            if effective_puw_context:
                from ..contrib.pyunitwizard_support import context as puw_ctx_manager
                with puw_ctx_manager(**effective_puw_context): return _run_digestion()
            return _run_digestion()

        wrapper.digestion_plan = plan
        return wrapper
    return deco

def _arg_digest_map(
    type_check=False,
    puw_context=None,
    profiling=_UNSET,
    **map_config
):
    return arg_digest(map=map_config, type_check=type_check, puw_context=puw_context, profiling=profiling)

arg_digest.map = _arg_digest_map
