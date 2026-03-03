from __future__ import annotations
import time
import threading
from typing import Callable, Any
from .logger import get_logger
from smonitor import signal

logger = get_logger()

class Registry:
    # kind -> name -> callable
    _pipelines: dict[str, dict[str, Callable[..., Any]]] = {}
    _lock = threading.RLock()

    @classmethod
    def register_pipeline(cls, kind: str, name: str, func: Callable[..., Any]) -> None:
        with cls._lock:
            cls._pipelines.setdefault(kind, {})
            cls._pipelines[kind][name] = func

    @classmethod
    def get_pipelines(cls, kind: str) -> dict[str, Callable[..., Any]]:
        with cls._lock:
            return dict(cls._pipelines.get(kind, {}))

    @classmethod
    @signal(tags=["pipeline"])
    def run(cls, kind: str, rules: list[str | Any], value: Any, ctx: Any) -> Any:
        logger.debug(f"Starting pipelines for kind='{kind}' on argument='{ctx.argname}'")
        pipelines = cls.get_pipelines(kind)
        current = value
        
        do_profile = getattr(ctx, "_profiling", False)

        for rule in rules or []:
            fn = None
            rule_name = str(rule)
            
            if isinstance(rule, str):
                fn = pipelines.get(rule)
                if fn is None:
                    logger.debug(f"Rule '{rule}' not found in kind='{kind}'. Available: {list(pipelines.keys())}")
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
    @signal(tags=["registry"], exception_level="DEBUG")
    def deco(fn: Callable[..., Any]):
        Registry.register_pipeline(kind, name, fn)
        return fn
    return deco


@signal(tags=["registry"], exception_level="DEBUG")
def get_pipelines(kind: str) -> dict[str, Callable[..., Any]]:
    return Registry.get_pipelines(kind)
