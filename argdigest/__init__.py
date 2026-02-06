"""
ArgDigest — flexible argument auditing and normalization for scientific libraries.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("argdigest")
except PackageNotFoundError:
    # Package is not installed
    try:
        from ._version import __version__
    except ImportError:
        __version__ = "0.0.0+unknown"

from ._private.smonitor import ensure_configured as _ensure_smonitor_configured

_ensure_smonitor_configured()

from .core.decorator import arg_digest
from .core.registry import register_pipeline, get_pipelines
from .core.argument_registry import argument_digest
from .core.config import DigestConfig
from .core.errors import (
    DigestError,
    DigestTypeError,
    DigestValueError,
    DigestInvariantError,
    DigestNotDigestedError,
    DigestNotDigestedWarning,
)

# Register standard pipelines
from . import pipelines

__all__ = [
    "arg_digest",
    "register_pipeline",
    "get_pipelines",
    "argument_digest",
    "DigestConfig",
    "pipelines",
    "DigestError",
    "DigestTypeError",
    "DigestValueError",
    "DigestInvariantError",
    "DigestNotDigestedError",
    "DigestNotDigestedWarning",
]
