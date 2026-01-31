from __future__ import annotations
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
        for rule in rules or []:
            fn = None
            
            # 1. If it's a string, look it up
            if isinstance(rule, str):
                fn = pipelines.get(rule)
                if fn is None:
                    logger.warning(f"Rule '{rule}' not found for kind='{kind}'. Skipping.")
                    continue
                logger.debug(f"Running rule '{rule}' on argument='{ctx.argname}'")
                current = fn(current, ctx)
                continue

            # 2. If it's a Pydantic Model (duck typing)
            if isinstance(rule, type) and hasattr(rule, "model_validate"):
                logger.debug(f"Running Pydantic model '{rule.__name__}' on argument='{ctx.argname}'")
                try:
                    current = rule.model_validate(current)
                except Exception as e:
                    # Provide rich context for pydantic errors
                    raise ValueError(f"Validation failed for argument '{ctx.argname}' against model {rule.__name__}: {e}") from e
                continue

            # 3. If it's a callable (direct function)
            if callable(rule):
                logger.debug(f"Running callable rule '{rule.__name__}' on argument='{ctx.argname}'")
                current = rule(current, ctx)
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

