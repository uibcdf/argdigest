from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

CATALOG = {
    "missing_digester": {
        "code": "ARGDIGEST-MISSING-DIGESTER",
        "source": "argdigest.digester",
        "category": "argument",
        "level": "WARNING",
    },
    "typecheck_skip": {
        "code": "ARGDIGEST-TYPECHECK-SKIP",
        "source": "argdigest.digester",
        "category": "argument",
        "level": "WARNING",
    },
}
