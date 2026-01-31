from __future__ import annotations

from typing import Any, Callable


class ArgumentRegistry:
    # argument name -> callable
    _digesters: dict[str, Callable[..., Any]] = {}

    @classmethod
    def register(cls, name: str, func: Callable[..., Any]) -> None:
        cls._digesters[name] = func

    @classmethod
    def get_all(cls) -> dict[str, Callable[..., Any]]:
        return dict(cls._digesters)

    @classmethod
    def clear(cls) -> None:
        cls._digesters.clear()


def argument_digest(name: str):
    """
    Decorator to register an argument digester by argument name.
    """
    def deco(fn: Callable[..., Any]):
        ArgumentRegistry.register(name, fn)
        return fn
    return deco
