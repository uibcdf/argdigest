from __future__ import annotations
import time
from typing import Callable, Any
from .logger import get_logger

logger = get_logger()

class Registry:
    # kind -> name -> callable
    _pipelines: dict[str, dict[str, Callable[..., Any]]] = {}

    @classmethod
    def register_pipeline(cls, kind: str, name: str, func: Callable[..., Any]) -> None:
        cls._pipelines.setdefault(kind, {})
        cls._pipelines[kind][name] = func

    @classmethod
    def get_pipelines(cls, kind: str) -> dict[str, Callable[..., Any]]:
        return cls._pipelines.get(kind, {})

    @classmethod
    def run(cls, kind: str, rules: list[str | Any], value: Any, ctx: Any) -> Any:
        """
        Run registered pipelines for given kind and rule names.
        Each pipeline may transform/validate the value and return it.
        Rules can be:
        - Strings: names of registered pipelines.
        - Callables: functions taking (value, ctx).
        - Pydantic Models: classes with .model_validate().
        """
        logger.debug(f"Starting pipelines for kind='{kind}' on argument='{ctx.argname}'")
        pipelines = cls._pipelines.get(kind, {})
        current = value
        
        # Check if profiling is active (we pass it via context or it could be global)
        # For now, let's assume it's an attribute in ctx or we check a global config
        # Actually, let's look for 'profiling' in ctx if it's there
        do_profile = getattr(ctx, "_profiling", False)

        for rule in rules or []:
            fn = None
            rule_name = str(rule)
            
            # 1. If it's a string, look it up
            if isinstance(rule, str):
                fn = pipelines.get(rule)
                if fn is None:
                    logger.warning(f"Rule '{rule}' not found for kind='{kind}'. Skipping.")
                    continue
                rule_name = f"{kind}.{rule}"
                logger.debug(f"Running rule '{rule_name}' on argument='{ctx.argname}'")
                
                start = time.perf_counter() if do_profile else 0
                current = fn(current, ctx)
                if do_profile:
                    duration = time.perf_counter() - start
                    ctx.audit_log.append({"rule": rule_name, "duration": duration})
                continue

            # 2. If it's a Pydantic Model (duck typing)
            if isinstance(rule, type) and hasattr(rule, "model_validate"):
                rule_name = f"Pydantic:{rule.__name__}"
                logger.debug(f"Running Pydantic model '{rule.__name__}' on argument='{ctx.argname}'")
                try:
                    start = time.perf_counter() if do_profile else 0
                    current = rule.model_validate(current)
                    if do_profile:
                        duration = time.perf_counter() - start
                        ctx.audit_log.append({"rule": rule_name, "duration": duration})
                except Exception as e:
                    raise ValueError(f"Validation failed for argument '{ctx.argname}' against model {rule.__name__}: {e}") from e
                continue

            # 3. If it's a callable (direct function)
            if callable(rule):
                rule_name = getattr(rule, "__name__", "anonymous_callable")
                logger.debug(f"Running callable rule '{rule_name}' on argument='{ctx.argname}'")
                start = time.perf_counter() if do_profile else 0
                current = rule(current, ctx)
                if do_profile:
                    duration = time.perf_counter() - start
                    ctx.audit_log.append({"rule": rule_name, "duration": duration})
                continue
            
            logger.warning(f"Unknown rule type {type(rule)} for argument='{ctx.argname}'. Skipping.")
        
        logger.debug(f"Finished pipelines for argument='{ctx.argname}'. Final value type: {type(current)}")
        return current


def register_pipeline(kind: str, name: str):
    """
    Decorator to register a pipeline function for a given kind and name.
    """
    def deco(fn: Callable[..., Any]):
        Registry.register_pipeline(kind, name, fn)
        return fn
    return deco


def get_pipelines(kind: str) -> dict[str, Callable[..., Any]]:
    return Registry.get_pipelines(kind)

