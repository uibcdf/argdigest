from __future__ import annotations


def emit_missing_digester(*, argname: str) -> None:
    import smonitor

    smonitor.emit(
        "WARNING",
        "",
        source="argdigest.digester",
        code="ARGDIGEST-MISSING-DIGESTER",
        category="argument",
        extra={"argname": argname},
    )


def emit_typecheck_skip() -> None:
    import smonitor

    smonitor.emit(
        "WARNING",
        "",
        source="argdigest.digester",
        code="ARGDIGEST-TYPECHECK-SKIP",
        category="argument",
        extra={},
    )
