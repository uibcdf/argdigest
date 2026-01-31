"""
Central configuration module for ArgDigest.
Use this module to set global defaults and configure logging.
"""

from .core.config import set_defaults, get_defaults
from .core.logger import configure_logging as setup_logging

__all__ = [
    "set_defaults",
    "get_defaults",
    "setup_logging",
]
