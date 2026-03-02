# Integrating Your Library

Use this page as a migration blueprint for existing codebases.

## Minimum viable integration (one afternoon)

If time is limited, focus on one tight slice: add `_argdigest.py`, migrate one
high-traffic API function, implement digesters for the two or three arguments
that create most support friction, and add tests for valid, invalid, and bypass
paths. This usually gives immediate consistency improvements without a large
migration.

## First principle

Treat ArgDigest adoption as an API-boundary refactor:
- move digestion logic out of business code,
- make behavior explicit and testable,
- keep one contract source for contributors.

## Phase 1: establish configuration

1. Add `mylib/_argdigest.py`.
2. Choose one digestion style (`package`, `registry`, or `decorator`).
3. Configure `strictness="warn"` for initial rollout.

Checkpoint:
- the package imports cleanly,
- one decorated function runs with digesters active.

## Phase 2: migrate high-value functions

Start with:
- public API entry points,
- functions that currently have repeated argument checks,
- functions with known user confusion around argument semantics.

Checkpoint:
- digestion logic is removed from function bodies in migrated modules.

## Phase 3: add normalization and pipelines

1. Add a standardizer if argument aliases exist.
2. Register reusable pipelines for repeated validations.
3. Keep semantic checks close to digestion contracts.

Checkpoint:
- alias handling is consistent across functions,
- repeated validation code is replaced by pipeline rules.

## Phase 4: harden behavior

1. Add tests for invalid and edge inputs.
2. Track missing-digester warnings.
3. Move to `strictness="error"` when ready.

Checkpoint:
- missing digesters are treated as integration defects,
- API behavior is stable and documented.

## Practical migration order

1. one module,
2. one argument family,
3. one subsystem at a time,
4. then global rollout.

## Expected gains during migration

As migration progresses, you should see less duplicated validation code in
business modules, more consistent behavior across similar entry points, and a
clearer support/debug path for invalid inputs.

## End-user communication

Even if end users do not know ArgDigest, they will see its effects through
validation messages. Include a short section in your host-library docs that
explains how to read these messages and how to report mismatches effectively.

## Next

Continue with [Examples](examples.md).
