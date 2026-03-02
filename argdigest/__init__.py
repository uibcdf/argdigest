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

from smonitor.integrations import ensure_configured as _ensure_smonitor_configured
from ._private.smonitor import PACKAGE_ROOT as _SMONITOR_PACKAGE_ROOT

_ensure_smonitor_configured(_SMONITOR_PACKAGE_ROOT)

from .core.decorator import arg_digest  # noqa: E402
from .core.registry import register_pipeline, get_pipelines  # noqa: E402
from .core.argument_registry import argument_digest  # noqa: E402
from .core.config import DigestConfig  # noqa: E402
from .core.errors import (  # noqa: E402
    DigestError,
    DigestTypeError,
    DigestValueError,
    DigestInvariantError,
    DigestNotDigestedError,
    DigestNotDigestedWarning,
)

# Register standard pipelines
from . import pipelines  # noqa: E402

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
