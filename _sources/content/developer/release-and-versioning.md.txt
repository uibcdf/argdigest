# Release and Versioning

ArgDigest versions do not use a `v` prefix.

## Release path to 1.0.0

Current roadmap stages are tracked in:
- `devguide/ROADMAP.md`
- `devguide/0.6.x_checklist.md`

## Pre-release checks

1. Tests pass.
2. Documentation reflects runtime behavior.
3. Public API changes are documented.
4. Examples and showcase remain valid.

## Practical release flow

Use this order for release preparation:

1. Finish feature/fix scope and merge pending documentation updates.
2. Run local gates (`pytest`, docs build).
3. Verify roadmap/checklist alignment in:
   - `devguide/ROADMAP.md`
   - `devguide/0.6.x_checklist.md`
4. Confirm version string is correct and changelog/release notes are ready.
5. Create the release commit/tag using numeric versions (no `v` prefix).
6. Validate published artifacts and docs after release.

## Post-release sanity

After publishing:
- verify installation paths (conda/pip) resolve expected version,
- verify key docs pages match the released behavior,
- monitor first integration feedback for regressions.

## Versioning principles

- Patch: bugfixes and non-breaking behavior corrections.
- Minor: new features without breaking documented API.
- Major: breaking API/contract changes.
