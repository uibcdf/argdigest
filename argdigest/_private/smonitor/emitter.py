from __future__ import annotations

from smonitor.integrations import DiagnosticBundle

from ...core.diagnostics import detailed_diagnostics, get_capture_policy
from .catalog import CATALOG, CODES, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)

warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve


def _fallback_warning(key="ARG-WARN-DIAGNOSTICS-001"):
    import warnings

    try:
        warnings.warn(CODES[key]["metadata_message"], RuntimeWarning)
    except Exception:
        # A promoted or broken fallback must not replace a native failure or
        # prevent a successful operation. The fixed warning was attempted.
        pass


def diagnostic_failure(error, *, stage, caller, argname):
    """Emit a catalog failure without collecting forbidden native error text."""
    try:
        from smonitor import emit

        entry = CATALOG["info"][
            "DigesterFailure" if stage == "digestion" else "PipelineFailure"
        ]
        facts = {"cause_exception_type": type(error).__name__[:256]}
        for name, value in (("caller", caller), ("argname", argname)):
            if type(value) is str:
                facts[name] = value[:256]
        extra = dict(facts)
        if detailed_diagnostics():
            extra["cause_message"] = str(error)
        options = {}
        policy = get_capture_policy()
        if policy is not None and not policy.extra:
            # The enclosing scope already carries approved caller facts. Keep
            # bounded library identity even though ordinary extras are disabled.
            options["safe_extra"] = facts
        emit(
            entry["level"],
            "",
            code=entry["code"],
            source=entry["source"],
            category=entry["category"],
            extra=extra,
            **options,
        )
    except Exception:
        _fallback_warning()


def type_check_skipped(caller):
    try:
        from smonitor.integrations import emit_from_catalog, merge_extra

        emit_from_catalog(
            CATALOG["warnings"]["TypeCheckSkippedWarning"],
            package_root=PACKAGE_ROOT,
            extra=merge_extra(META, {"caller": caller}),
        )
    except Exception:
        _fallback_warning("ARG-WARN-TYPECHECK-001")
