from __future__ import annotations

from functools import wraps
import inspect
import threading
import warnings
from typing import Any, Callable

from .registry import Registry
from .context import Context
from .utils import bind_arguments, build_call
from .argument_loader import load_argument_digesters, resolve_standardizer
from .function_loader import load_domains, load_function_contracts, load_normalization
from .normalization import NormalizationRegistry, apply_normalization
from .function_contract import ContractRegistry, check_contract, default_contract
from .argument_registry import ArgumentRegistry
from .config import resolve_config, DigestConfig, get_env_config_module
from collections.abc import Mapping

from .errors import (
    ArgumentConsistencyError,
    StandardizerContractError,
    FunctionContractError,
    DigestNotDigestedError,
    DigestNotDigestedWarning,
    FunctionContractWarning,
    MissingArgumentError,
    UnknownArgumentError,
)
from .logger import get_logger
from smonitor import signal
from depdigest import dep_digest

from dataclasses import dataclass, field

_UNSET = object()
logger = get_logger()


def _resolve_owner_module(fn: Callable[..., Any], args: tuple[Any, ...]) -> str:
    """Resolve the logical owner module of a decorated callable.

    For methods (``__qualname__`` is ``Class.method``) the logical owner is the
    *runtime* class of the bound instance, which may differ from the module where
    the function was physically defined — e.g. classes assembled from mixins
    living in separate modules. Resolving from ``type(self)`` reports the class's
    real module without requiring module-level ``__name__`` spoofing in the
    defining files. Free functions keep their defining module.
    """
    qualname = getattr(fn, "__qualname__", "") or ""
    if args and "." in qualname and "<locals>" not in qualname:
        owner = type(args[0])
        if isinstance(owner, type) and hasattr(owner, fn.__name__):
            module = getattr(owner, "__module__", None)
            if isinstance(module, str) and module:
                return module
    return fn.__module__

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
    signature: inspect.Signature | None = None
    # Axis 1: the function argument contract.
    normalization: "NormalizationRegistry | None" = None
    contracts: "ContractRegistry | None" = None
    domains: dict[str, Any] = field(default_factory=dict)
    unknown_argument: str = "error"
    # Precomputed once per decorated function; rebuilding it per call was measurable.
    signature_parameter_names: frozenset[str] = field(default_factory=frozenset)
    # Whether calling back with `**bound` would lose part of the call. Decided once at
    # decoration time so the common signature keeps the single dict unpack it had.
    requires_call_shape: bool = False


def _hashable_source(source: Any) -> Any:
    """lru_cache keys must be hashable; a list of sources becomes a tuple."""

    if isinstance(source, list):
        return tuple(source)
    return source


_CONTRACT_ERRORS = {
    "unknown_argument": UnknownArgumentError,
    "missing_argument": MissingArgumentError,
    "mutually_exclusive": ArgumentConsistencyError,
    "co_required": ArgumentConsistencyError,
}


def _invoke(plan: "DigestionPlan", fn_to_wrap: Callable[..., Any],
            bound: dict[str, Any]) -> Any:
    """Call the wrapped function with the arguments digestion produced.

    Most signatures can be called back with `**bound`, and are: one dict unpack. A
    signature carrying `*args` or a positional-only parameter cannot, because neither
    has a keyword form, so its call is reconstructed instead. Which of the two applies
    is a property of the signature, decided once at decoration time.
    """

    if not plan.requires_call_shape or plan.signature is None:
        return fn_to_wrap(**bound)
    call_args, call_kwargs = build_call(plan.signature, bound)
    return fn_to_wrap(*call_args, **call_kwargs)


def _enforce_function_contract(plan: "DigestionPlan", caller: str, fn: Callable[..., Any],
                               bound: dict[str, Any], extras: dict[str, Any],
                               supplied: set[str]) -> None:
    """Axis 1: hold the call to the function's argument contract.

    Runs after the standardizer, so aliases have already become their canonical names
    and a legitimate alias is never mistaken for a typo, and before digestion, because
    there is no point validating the value of an argument that should not be there.
    """

    if plan.contracts is None or plan.signature is None:
        return

    contract = plan.contracts.resolve(caller)
    if contract is None:
        contract = default_contract(caller, plan.var_keyword_name is not None)

    signature_parameters = plan.signature_parameter_names
    candidate_extras = list(extras)
    if plan.var_keyword_name is not None:
        # Only a function declaring **kwargs can carry extras inside `bound`; for a closed
        # signature they were already set aside by bind_arguments, so scanning `bound`
        # would be a guaranteed-empty pass over every argument on every call.
        candidate_extras.extend(name for name in bound if name not in signature_parameters)

    # The overwhelmingly common call is a correct one to a closed signature: no extra
    # keyword, and a contract with nothing else to assert. There is then nothing that
    # could be violated, so the stage costs one lookup and returns.
    if not candidate_extras and not contract.has_rules_beyond_admission():
        return

    defaulted = signature_parameters - supplied
    present = (set(bound) | set(extras)) - defaulted

    violations = check_contract(
        contract, caller, signature_parameters, candidate_extras, plan.domains, present,
        bound=bound)
    if not violations:
        return

    for violation in violations:
        ctx_error = Context(function_name=caller, argname=violation.keyword or "unknown",
                            value=bound.get(violation.keyword) if violation.keyword else None,
                            all_args=bound)
        # A contract naming a domain nobody registered is a declaration bug in the
        # consumer library, not a mistake by whoever made the call. Silencing it would
        # quietly weaken every check that contract was meant to perform.
        if violation.kind == "unknown_domain":
            raise FunctionContractError(violation.message, context=ctx_error, hint=violation.hint)
        if plan.unknown_argument == "ignore":
            continue
        if plan.unknown_argument == "warn":
            warnings.warn(FunctionContractWarning(
                message=violation.message, context=ctx_error, hint=violation.hint))
            continue
        raise _CONTRACT_ERRORS[violation.kind](
            violation.message, context=ctx_error, hint=violation.hint)


def arg_digest(
    *,
    kind: str | None = None,
    rules: list[str] | None = None,
    map: dict[str, dict] | None = None,
    digestion_source: str | list[str] | None | object = _UNSET,
    digestion_style: str | object = _UNSET,
    standardizer: Any | object = _UNSET,
    strictness: str | object = _UNSET,
    unknown_argument: str | object = _UNSET,
    function_source: str | list[str] | None | object = _UNSET,
    normalization_source: str | list[str] | None | object = _UNSET,
    domain_source: str | list[str] | None | object = _UNSET,
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
        eff_function_source = cfg.function_source if function_source is _UNSET else function_source
        eff_domain_source = cfg.domain_source if domain_source is _UNSET else domain_source
        eff_normalization_source = (cfg.normalization_source
                                    if normalization_source is _UNSET
                                    else normalization_source)
        eff_unknown_argument = _normalize_strictness(
            cfg.unknown_argument if unknown_argument is _UNSET else unknown_argument)
        
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

        # Axis 1 declarations. lru_cache needs hashable sources.
        contracts = load_function_contracts(_hashable_source(eff_function_source))
        domains = load_domains(_hashable_source(eff_domain_source))
        normalization = load_normalization(_hashable_source(eff_normalization_source))

        # Inspect signature once
        signature = inspect.signature(fn)
        var_keyword_name = next((p.name for p in signature.parameters.values() if p.kind == inspect.Parameter.VAR_KEYWORD), None)
        # `*args` has no keyword form and a positional-only parameter refuses one, so
        # calling back with `**bound` would lose them. Only those two signatures pay for
        # the reconstruction.
        requires_call_shape = any(
            p.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.POSITIONAL_ONLY)
            for p in signature.parameters.values())

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
            var_keyword_name=var_keyword_name,
            signature=signature,
            normalization=normalization,
            contracts=contracts,
            domains=domains,
            unknown_argument=eff_unknown_argument,
            signature_parameter_names=frozenset(
                name for name in signature.parameters if name != var_keyword_name),
            requires_call_shape=requires_call_shape,
        )

        @wraps(fn)
        @signal(tags=["digestion"], exception_level="DEBUG")
        def wrapper(*args: Any, **kwargs: Any):
            # Fast-path check: if skip_digestion is passed in kwargs, bypass everything O(1)
            if kwargs.get(plan.skip_param, False):
                return fn_to_wrap(*args, **kwargs)

            logger.debug(f"Digesting arguments for {fn.__name__}")
            if plan.profiling:
                wrapper.audit_log = []

            
            def _run_digestion():
                extras: dict[str, Any] = {}
                # Which names the caller actually wrote, as opposed to the ones
                # `bind_arguments` fills in from the signature's defaults.
                supplied: set[str] = set()
                bound = bind_arguments(fn, *args, sig=plan.signature,
                                       var_keyword_name=plan.var_keyword_name,
                                       extras_out=extras, supplied_out=supplied, **kwargs)
                supplied.update(extras)
                if bound.get(plan.skip_param, False):
                    return _invoke(plan, fn_to_wrap, bound)

                caller = f"{_resolve_owner_module(fn, args)}.{fn.__name__}"

                if plan.var_keyword_name and plan.var_keyword_name in bound:

                    extra = bound.pop(plan.var_keyword_name) or {}
                    if isinstance(extra, dict):
                        bound.update(extra)
                        supplied.discard(plan.var_keyword_name)
                        supplied.update(extra)

                if plan.normalization:
                    bound = apply_normalization(plan.normalization, caller, bound, supplied)

                if plan.standardizer:
                    standardized = plan.standardizer(caller, bound)
                    if not isinstance(standardized, Mapping):
                        raise StandardizerContractError(
                            f"it returned {type(standardized).__name__} instead of a "
                            "mapping of arguments",
                            context=Context(function_name=caller, argname="-",
                                            value=standardized, all_args=bound),
                            hint="A standardizer takes (caller, kwargs) and returns the "
                                 "mapping; forgetting the return statement is the usual "
                                 "cause.",
                        )
                    bound = dict(standardized)

                # Axis 1 runs here: after names are canonical, before any value is
                # digested.
                supplied = set(kwargs)
                if plan.signature is not None:
                    positional = list(plan.signature.parameters)[:len(args)]
                    supplied.update(positional)
                _enforce_function_contract(plan, caller, fn, bound, extras, supplied)

                digested: dict[str, Any] = {}
                visiting_path: list[str] = []

                def gut(argname: str) -> None:
                    if argname in digested:
                        return
                    if argname in visiting_path:
                        ctx_error = Context(function_name=fn.__name__, argname=argname, value=bound.get(argname), all_args=bound)
                        raise DigestNotDigestedError(f"Cycle: {' -> '.join(visiting_path + [argname])}", context=ctx_error)
                    visiting_path.append(argname)

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

                return _invoke(plan, fn_to_wrap, bound)

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
