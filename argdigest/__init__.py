"""
ArgDigest — flexible argument auditing and normalization for scientific libraries.
"""

from .core.decorator import digest
from .core.registry import register_pipeline, get_pipelines
from .core.argument_registry import argument_digest
from .core.config import DigestConfig, set_defaults, get_defaults
from .core.errors import (
    DigestError,
    DigestTypeError,
    DigestValueError,
    DigestInvariantError,
    DigestNotDigestedError,
    DigestNotDigestedWarning,
)

__all__ = [
    "digest",
    "register_pipeline",
    "get_pipelines",
    "argument_digest",
    "DigestConfig",
    "set_defaults",
    "get_defaults",
    "DigestError",
    "DigestTypeError",
    "DigestValueError",
    "DigestInvariantError",
    "DigestNotDigestedError",
    "DigestNotDigestedWarning",
]
