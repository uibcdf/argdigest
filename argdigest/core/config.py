from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from typing import Any


@dataclass(frozen=True)
class DigestConfig:
    digestion_source: str | list[str] | None = None
    digestion_style: str = "auto"
    standardizer: Any = None
    strictness: str = "warn"
    skip_param: str = "skip_digestion"


_DEFAULTS: DigestConfig = DigestConfig()


def set_defaults(config: DigestConfig) -> None:
    global _DEFAULTS
    _DEFAULTS = config


def get_defaults() -> DigestConfig:
    return _DEFAULTS


def _from_module(module_path: str) -> DigestConfig:
    module = import_module(module_path)
    return DigestConfig(
        digestion_source=getattr(module, "DIGESTION_SOURCE", None),
        digestion_style=getattr(module, "DIGESTION_STYLE", "auto"),
        standardizer=getattr(module, "STANDARDIZER", None),
        strictness=getattr(module, "STRICTNESS", "warn"),
        skip_param=getattr(module, "SKIP_PARAM", "skip_digestion"),
    )


def resolve_config(config: Any) -> DigestConfig:
    if config is None:
        return get_defaults()
    if isinstance(config, DigestConfig):
        return config
    if isinstance(config, str):
        return _from_module(config)
    raise TypeError("config must be a DigestConfig, a module path string, or None")
