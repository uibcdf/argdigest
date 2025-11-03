"""
ArgDigest — flexible argument auditing and normalization for scientific libraries.
"""

from .core.decorator import digest
from .core.registry import register_pipeline, get_pipelines
from .core.errors import DigestError, DigestTypeError, DigestValueError, DigestInvariantError

__all__ = [
    "digest",
    "register_pipeline",
    "get_pipelines",
    "DigestError",
    "DigestTypeError",
    "DigestValueError",
    "DigestInvariantError",
]

