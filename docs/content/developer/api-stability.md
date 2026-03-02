# API Stability

ArgDigest aims for stable public contracts as it approaches `1.0.0`.

## Public surface

Treat these as public API:
- `arg_digest`
- `argument_digest`
- `register_pipeline`
- documented error classes
- documented config behavior

## Stability rules

- Avoid renaming public parameters without a migration path.
- Avoid changing precedence rules silently.
- Keep documented behavior synchronized with runtime behavior.

## Breaking changes policy

Before `1.0.0`, any planned breaking change must:
1. be documented explicitly,
2. include migration guidance,
3. be covered by tests and release notes.
