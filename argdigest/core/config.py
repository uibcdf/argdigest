from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any


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
    """
    Set the global default configuration for ArgDigest.
    
    Can be called with a DigestConfig object:
        set_defaults(DigestConfig(strictness="error"))
        
    Or with keyword arguments to update specific fields:
        set_defaults(strictness="error", digestion_source="mylib")
    """
    global _DEFAULTS
    
    if config is not None:
        if kwargs:
            raise ValueError("Cannot specify both 'config' object and keyword arguments.")
        _DEFAULTS = config
        return

    if kwargs:
        # Update existing defaults with new values
        from dataclasses import replace
        _DEFAULTS = replace(_DEFAULTS, **kwargs)


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
        puw_context=getattr(module, "PUW_CONTEXT", None),
        profiling=getattr(module, "PROFILING", False),
    )


def load_from_file(file_path: str) -> DigestConfig:
    """
    Loads configuration from a YAML or JSON file.
    """
    import os
    import json

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    with open(file_path, "r") as f:
        if ext in (".yaml", ".yml"):
            try:
                import yaml
                data = yaml.safe_load(f)
            except ImportError:
                raise ImportError("PyYAML is required to load YAML configuration files.")
        elif ext == ".json":
            data = json.load(f)
        else:
            raise ValueError(f"Unsupported configuration file format: {ext}")

    if not isinstance(data, dict):
        raise ValueError("Configuration file must contain a top-level dictionary.")

    # Convert keys to lowercase to match DigestConfig fields
    # and map legacy MolSysMT names if necessary (optional, but good for consistency)
    config_data = {k.lower(): v for k, v in data.items()}
    
    return DigestConfig(**config_data)


def resolve_config(config: Any) -> DigestConfig:
    if config is None:
        return get_defaults()
    if isinstance(config, DigestConfig):
        return config
    if isinstance(config, str):
        return _from_module(config)
    raise TypeError("config must be a DigestConfig, a module path string, or None")
