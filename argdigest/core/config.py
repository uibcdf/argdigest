from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class DigestConfig:
    digestion_source: str | list[str] | None = None
    digestion_style: str = "auto"
    standardizer: Any = None
    strictness: str = "warn"
    skip_param: str = "skip_digestion"
    puw_context: dict[str, Any] | None = None
    profiling: bool = False


_DEFAULTS: DigestConfig = DigestConfig()


def set_defaults(config: DigestConfig | None = None, **kwargs: Any) -> None:
    global _DEFAULTS
    
    if config is not None:
        if kwargs:
            raise ValueError("Cannot specify both 'config' object and keyword arguments.")
        _DEFAULTS = config
        return

    if kwargs:
        from dataclasses import replace
        _DEFAULTS = replace(_DEFAULTS, **kwargs)
    
    # Invalidate cache if defaults change
    resolve_config.cache_clear()


def get_defaults() -> DigestConfig:
    return _DEFAULTS

@lru_cache(maxsize=128)
def _from_module(module_path: str) -> DigestConfig:
    module = import_module(module_path)
    return DigestConfig(
        digestion_source=getattr(module, "DIGESTION_SOURCE", None),
        digestion_style=getattr(module, "DIGESTION_STYLE", "auto"),
        standardizer=getattr(module, "STANDARDIZER", None),
        strictness=getattr(module, "STRICTNESS", "warn"),
        skip_param=getattr(module, "SKIP_PARAM", "skip_digestion"),
        puw_context=getattr(module, "PUW_CONTEXT", None),
        profiling=getattr(module, "PROFILING", False),
    )

def load_from_file(path: str | Path) -> DigestConfig:
    """
    Load configuration from a Python, YAML, or JSON file path.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    
    ext = path.suffix.lower()
    
    if ext == ".py":
        import importlib.util
        spec = importlib.util.spec_from_file_location("_argdigest_ext", str(path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load config from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return DigestConfig(
            digestion_source=getattr(module, "DIGESTION_SOURCE", None),
            digestion_style=getattr(module, "DIGESTION_STYLE", "auto"),
            standardizer=getattr(module, "STANDARDIZER", None),
            strictness=getattr(module, "STRICTNESS", "warn"),
            skip_param=getattr(module, "SKIP_PARAM", "skip_digestion"),
            puw_context=getattr(module, "PUW_CONTEXT", None),
            profiling=getattr(module, "PROFILING", False),
        )
    
    if ext in (".yaml", ".yml"):
        import yaml
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return DigestConfig(**data)
    
    if ext == ".json":
        import json
        with open(path, "r") as f:
            data = json.load(f)
        return DigestConfig(**data)
    
    raise ValueError(f"Unsupported config file extension: {ext}")

def resolve_config(config: Any) -> DigestConfig:
    if config is None:
        return get_defaults()
    if isinstance(config, DigestConfig):
        return config
    if isinstance(config, str):
        return _from_module(config)
    raise TypeError("config must be a DigestConfig, a module path string, or None")

# Export a cached version of resolve_config too
resolve_config = lru_cache(maxsize=128)(resolve_config)