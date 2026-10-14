# SMonitor integration

ArgDigest uses SMonitor as the single diagnostics layer.

The application-owned source setup in `uibcdf/argdigest#32` detects the public
declaration-only bundle capability delivered in SMonitor >=0.20.0 under
`uibcdf/smonitor#48` and `uibcdf/smonitor#50`. When available,
the root registers catalogs and uses nonbootstrapping bundle/direct emission.
Applications call `configure_diagnostics()` explicitly; the CLI performs that
step itself. Older supported providers retain their existing initialization and
refuse an explicit registration-only request. Do not present this unreleased
ArgDigest integration as a shipped dependency guarantee or copy the provider's
warning implementation. DepDigest is imported at the optional Beartype use
boundary rather than while exporting the core API.

Qualification uses `tests/test_diagnostic_registration.py` with
`--require-registration-only`: a missing provider capability is a failure in
that gate, while ordinary compatibility checks on old providers may skip the
capability-specific cases. The future release must select a published qualified
provider and a new committed version/plan; existing 0.15.0 artifacts and receipts
remain immutable.

Public-provider receiving on 2026-10-14 uses SMonitor 0.21.0 and DepDigest
0.15.1 with an installed private ArgDigest wheel in a fresh Linux/Python 3.14.8
environment. The strict suite passes 390 tests; one sibling-source collective
case is unavailable. Installed origins/archive bytes and pip check pass.
`evidence/registration_only_receiving_2026-10-14.json` records the boundary;
new exact ArgDigest Conda/release qualification remains pending.

The follow-up #32 review requires `--require-registration-only` as well as
`--require-scoped-capture` in the maintained installed profile, using public
SMonitor 0.21.0 / DepDigest 0.15.1. Its injected-unavailability guard executes
that profile and proves a missing capability cannot pass as a skipped case.
Fresh-process controls cover owned handlers, repeated registration and explicit
provider-policy override. Final private-wheel receiving passes 393 tests with
one unavailable sibling-source case; all eight registration cases execute.
See `evidence/registration_only_final_review_2026-10-14.json`.

SMonitor is a runtime dependency (hard dependency) in ArgDigest releases.

## Files

- `argdigest/_smonitor.py`
- `argdigest/_private/smonitor/catalog.py`
- `argdigest/_private/smonitor/meta.py`

## Rules

- Emit through catalog entries only.
- Keep user messages explicit and helpful.
- Keep URLs in `meta.py` so hints remain consistent.
- Keep `CODES` and `SIGNALS` wired from `argdigest/_private/smonitor/catalog.py` as the single source of truth.
- Do not silence emission failures with `except Exception: pass`; use a fallback warning/log instead.

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
