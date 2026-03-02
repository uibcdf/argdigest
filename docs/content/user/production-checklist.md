# Production Checklist

Use this checklist before releasing a library that integrates ArgDigest.

## Integration contract

Before release, ensure the integration contract is explicit. `_argdigest.py`
should exist, be documented for contributors, and reflect a stable digestion
style choice. `strictness` should also be intentional: mature code paths are
usually expected to run with `error`.

## Runtime behavior

Public API entry points should be decorated where needed, aliases should be
normalized consistently, and repeated validation semantics should be expressed
through reusable pipeline rules instead of scattered inline checks.

## Testing

Tests should cover both happy paths and invalid input behavior for migrated
functions. Missing-digester behavior must be explicitly tested, and at least one
smoke test should validate the full decorated call flow end to end.

## Diagnostics and docs

Error messages should include actionable context, and documentation/examples must
match current runtime behavior. Showcase pages are especially important because
integrators use them as copy/adaptation references.

## Release readiness

Release is ready when local tests pass, documentation builds cleanly, and
migration notes for downstream integrators are updated and coherent with the
current contract.
