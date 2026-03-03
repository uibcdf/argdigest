# API Stability

ArgDigest aims for stable public contracts as it approaches `1.0.0`.

## Public surface

Treat these as public API:
- `arg_digest`
- `arg_digest.map`
- `argument_digest`
- `register_pipeline`
- `get_pipelines`
- `DigestConfig`
- documented error classes
- documented config behavior

The exported surface is anchored by `argdigest.__all__` and protected by
contract tests in `tests/test_api_contract.py`.

## Stability rules

- Avoid renaming public parameters without a migration path.
- Avoid changing precedence rules silently.
- Keep documented behavior synchronized with runtime behavior.
- Keep callable signatures stable across patch/minor releases in `0.7.x`.
- Treat changes to `argdigest.__all__` as API changes that require explicit review.

## Breaking changes policy

Before `1.0.0`, any planned breaking change must:
1. be documented explicitly,
2. include migration guidance,
3. be covered by tests and release notes.
4. be reflected in `devguide/0.7.x_checklist.md` before merge.
