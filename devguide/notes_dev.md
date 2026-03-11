# Development Notes

## Current state snapshot

- Current stabilization tag: `0.9.2` (final pre-1.0 checkpoint).
- Core decorator: `arg_digest` supports argument-centric, pipeline-centric, and mixed modes.
- Config model: explicit args, config module (`_argdigest.py`), env override (`ARGDIGEST_CONFIG`), and auto-discovery.
- Diagnostics: catalog-backed errors/warnings integrated with smonitor.
- Optional integrations: beartype, pydantic, pyunitwizard.
- Examples: `examples/packlib` and `examples/reglib` used for smoke tests and docs.
- Packaging uses setuptools package discovery (`include = ["argdigest*"]`) to keep
  subpackages in release wheels.
- CI/docs workflows include strict import smoke checks that fail hard on import errors.
- CLI includes `argdigest health-check` for ecosystem diagnostics.
- Current local test status baseline: full suite green.

## Test status

- Full suite currently passes.
- Known warning pattern: tests using pipelines without digesters may emit
  `DigestNotDigestedWarning` when strictness is `warn`.

## Recent implementation note

- Added `argdigest.core.caller.normalize_caller`, `argdigest.core.caller.caller_matches`, `argdigest.core.caller.caller_is_one_of`, and `argdigest.core.caller.caller_startswith` as lightweight helper APIs for downstream digester authors.
- What changed in practice: downstream digesters can now express callable-specific optional semantics without open-coding fragile string logic such as repeated `caller.endswith(...)` or ad-hoc `caller.startswith(...)` branches.
- Why this was necessary: MolSysMT now exposes `MolSysBuilder` and `build.editable(...)` as normal public APIs. Those APIs legitimately accept values such as `molecular_system=None`, `atom_type=None`, `group_type=None`, or `entity_name=None` depending on the callable. Treating these as exceptional cases outside digestion would have weakened both ArgDigest and the downstream API contract.
- Design decision: the correct place to solve this is the digestion layer, not the downstream API. ArgDigest therefore grows a slightly richer caller helper surface while keeping the public top-level API stable.
- These helpers remain outside the top-level public surface so the stable `argdigest.__all__` contract does not change during the pre-1.0 hardening window.

## Open technical items

- Keep collective status aligned with sibling repos and `../molsyssuite/devguide/collective_v1_checklist.md`.
- Hold `1.0.0` tag until explicit release-owner confirmation.

## 1.0.0 path alignment

- `0.6.x`: integration hardening (closed).
- `0.7.x`: API freeze (closed).
- `0.8.x`: release candidate stabilization (closed).
- `0.9.x`: RC consolidation (active).
- `1.0.0`: stable release.

See `devguide/ROADMAP.md` for full milestones and exit criteria.
