import logging
import sys
from typing import Optional, Any

# Default logger name
LOGGER_NAME = "argdigest"

def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)

def configure_logging(level: int | str = logging.INFO, stream: Optional[Any] = None) -> None:
    """
    Simple helper to configure the argdigest logger.
    """
    logger = get_logger()
    logger.setLevel(level)
    
    # Avoid adding multiple handlers if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(stream or sys.stderr)
    formatter = logging.Formatter(
        "[%(name)s] %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

from typing import Any  # fix imports
