"""
ArgDigest — flexible argument auditing and normalization for scientific libraries.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("argdigest")
except PackageNotFoundError:
    # Package is not installed
    try:
        from ._version import __version__
    except ImportError:
        __version__ = "0.0.0+unknown"

from .diagnostics import (
    _initialize_diagnostics,
    configure_diagnostics,
    register_diagnostics,
)

_initialize_diagnostics()

# Register standard pipelines
from . import pipelines  # noqa: E402
from .core.argument_registry import argument_digest  # noqa: E402
from .core.config import DigestConfig  # noqa: E402
from .core.decorator import arg_digest  # noqa: E402
from .core.errors import (  # noqa: E402
    ArgumentConsistencyError,
    DigestError,
    DigestInvariantError,
    DigestNotDigestedError,
    DigestNotDigestedWarning,
    DigestTypeError,
    DigestValueError,
    FunctionContractError,
    FunctionContractWarning,
    MissingArgumentError,
    StandardizerContractError,
    UnknownArgumentError,
)
from .core.function_contract import (  # noqa: E402
    Domain,
    FunctionContract,
    describe_contract,
)
from .core.normalization import (  # noqa: E402
    AliasTable,
    describe_normalization,
)
from .core.registry import get_pipelines, register_pipeline  # noqa: E402

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
    "Domain",
    "FunctionContract",
    "FunctionContractError",
    "FunctionContractWarning",
    "UnknownArgumentError",
    "MissingArgumentError",
    "ArgumentConsistencyError",
    "describe_contract",
    "AliasTable",
    "describe_normalization",
    "StandardizerContractError",
    "register_diagnostics",
    "configure_diagnostics",
]
