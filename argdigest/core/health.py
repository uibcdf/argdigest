from __future__ import annotations

import importlib
import importlib.util
from typing import Any

import smonitor

from .._private.smonitor import CATALOG
from .._private.smonitor.emitter import resolve
from .context import Context
from .errors import DigestTypeError


def run_health_check() -> dict[str, dict[str, Any]]:
    """
    Run an ecosystem-oriented health check for ArgDigest integration points.
    """
    report: dict[str, dict[str, Any]] = {}

    # smonitor integration wiring
    try:
        from smonitor.integrations import ensure_configured
        from .._private.smonitor import PACKAGE_ROOT

        ensure_configured(PACKAGE_ROOT)
        report["smonitor"] = {"ok": True, "detail": "configured"}
    except Exception as exc:
        report["smonitor"] = {"ok": False, "detail": repr(exc)}

    # depdigest hard dependency presence
    try:
        importlib.import_module("depdigest")
        report["depdigest"] = {"ok": True, "detail": "imported"}
    except Exception as exc:
        report["depdigest"] = {"ok": False, "detail": repr(exc)}

    # optional dependency (informational only)
    has_puw = importlib.util.find_spec("pyunitwizard") is not None
    report["pyunitwizard_optional"] = {
        "ok": True,
        "detail": "available" if has_puw else "not installed (optional)",
    }

    # catalog integrity + machine-readable fields
    try:
        ctx = Context(function_name="health.check", argname="value", value="bad", all_args={})
        err = DigestTypeError("health", context=ctx, hint="health hint")
        code = CATALOG["exceptions"]["DigestTypeError"]["code"]
        msg = resolve(code=code, extra={"argname": "value", "message": "health", "caller": "health.check", "hint": "health hint"})
        ok = bool(err.code) and bool(err.hint) and bool(msg)
        report["diagnostics"] = {"ok": ok, "detail": f"code={err.code}"}
    except Exception as exc:
        report["diagnostics"] = {"ok": False, "detail": repr(exc)}

    # profile coherence (user vs dev messaging)
    previous_profile = "user"
    try:
        previous_profile = getattr(getattr(smonitor, "_config", object()), "profile", "user")
    except Exception:
        previous_profile = "user"

    try:
        extra = {"argname": "value", "message": "health", "caller": "health.check", "hint": "health hint"}
        smonitor.configure(profile="user")
        msg_user = resolve(code=CATALOG["exceptions"]["DigestTypeError"]["code"], extra=extra)
        smonitor.configure(profile="dev")
        msg_dev = resolve(code=CATALOG["exceptions"]["DigestTypeError"]["code"], extra=extra)
        report["profiles"] = {
            "ok": msg_user != msg_dev,
            "detail": "user/dev differ" if msg_user != msg_dev else "user/dev identical",
        }
    except Exception as exc:
        report["profiles"] = {"ok": False, "detail": repr(exc)}
    finally:
        try:
            smonitor.configure(profile=previous_profile)
        except Exception:
            smonitor.configure(profile="user")

    return report
