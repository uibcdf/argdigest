from __future__ import annotations
from typing import Callable, Any

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
    def run(cls, kind: str, rules: list[str], value: Any, ctx: Any) -> Any:
        """
        Run registered pipelines for given kind and rule names.
        Each pipeline may transform/validate the value and return it.
        """
        pipelines = cls._pipelines.get(kind, {})
        current = value
        for rule in rules or []:
            fn = pipelines.get(rule)
            if fn is None:
                continue
            current = fn(current, ctx)
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

