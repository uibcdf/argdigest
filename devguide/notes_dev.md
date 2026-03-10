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

- Added `argdigest.core.caller.normalize_caller`, `argdigest.core.caller.caller_matches`, and `argdigest.core.caller.caller_is_one_of` as lightweight helper APIs for downstream digester authors.
- Reason: several MolSysMT digesters branch on caller-specific semantics and repeatedly had to defend against `caller=None` or callable-based direct invocation during targeted coverage work.
- These helpers are intentionally kept outside the top-level public surface so the stable `argdigest.__all__` contract does not change during the pre-1.0 hardening window.

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
