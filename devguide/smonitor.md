# SMonitor integration

ArgDigest uses SMonitor as the single diagnostics layer.

SMonitor is a runtime dependency (hard dependency) in ArgDigest releases.

## Files

- `argdigest/_smonitor.py`
- `argdigest/_private/smonitor/catalog.py`
- `argdigest/_private/smonitor/meta.py`

## Rules

- Emit through catalog entries only.
- Keep user messages explicit and helpful.
- Keep URLs in `meta.py` so hints remain consistent.

## Telemetry & Traceability

Starting from v0.5.0, ArgDigest is fully instrumented with `@smonitor.signal` to provide transparent execution context.

**Instrumented areas:**
- **Digestion Wrapper**: The core `@arg_digest` decorator logic is traced.
- **Pipeline Registry**: `Registry.run` emits signals when executing coercers and validators.
- **Diagnostics**: Missing digesters trigger catalog-driven events with hints.

## Exception signal level

The top-level `@signal` applied in `argdigest.core.decorator.arg_digest`
uses `exception_level="DEBUG"`.

Rationale:
- digestion routinely probes alternative coercion/validation paths;
- recoverable internal exceptions are expected control-flow signals;
- surfacing those probes as `ERROR` would create noisy traces for QA and users.
