PROFILE = "user"

SMONITOR = {
    "level": "WARNING",
    "trace_depth": 3,
    "capture_warnings": False,
    "capture_logging": True,
    "theme": "plain",
}

PROFILES = {
    "user": {
        "level": "WARNING",
    },
    "dev": {
        "level": "INFO",
        "show_traceback": True,
    },
    "qa": {
        "level": "INFO",
        "show_traceback": True,
    },
    "agent": {
        "level": "WARNING",
    },
    "debug": {
        "level": "DEBUG",
        "show_traceback": True,
    },
}

# Keep catalog templates as the single source of truth.
from argdigest._private.smonitor.catalog import CODES, SIGNALS  # noqa: E402,F401
