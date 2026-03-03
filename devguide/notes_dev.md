# Development Notes

## Current state snapshot

- Core decorator: `arg_digest` supports argument-centric, pipeline-centric, and mixed modes.
- Config model: explicit args, config module (`_argdigest.py`), and auto-discovery.
- Diagnostics: catalog-backed errors/warnings integrated with smonitor.
- Optional integrations: beartype, pydantic, pyunitwizard.
- Examples: `examples/packlib` and `examples/reglib` used for smoke tests and docs.
- Packaging uses setuptools package discovery (`include = ["argdigest*"]`) to keep
  subpackages in release wheels.
- CI/docs workflows include strict import smoke checks that fail hard on import errors.
- Current local coverage baseline: ~96%.

## Test status

- Full suite currently passes.
- Known warning pattern: tests using pipelines without digesters may emit
  `DigestNotDigestedWarning` when strictness is `warn`.

## Open technical items

- Public API export consistency (`argdigest.core.__all__`).
- Warning-noise strategy in tests and examples.
- Keep conda/devtools and docs synchronized with release workflow.
- Keep release tags and docs deployment synchronized after workflow changes.

## 1.0.0 path alignment

- `0.6.x`: integration hardening (closed).
- `0.7.x`: API freeze (closed).
- `0.9.x`: release candidate stabilization (active).
- `1.0.0`: stable release.

See `devguide/ROADMAP.md` for full milestones and exit criteria.
