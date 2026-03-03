# ArgDigest Roadmap to 1.0.0

This roadmap defines the execution path from the current series to a stable `1.0.0` release.
Version labels intentionally do **not** use a `v` prefix.

## Release Strategy

The path to `1.0.0` is split into four stabilization stages:

1. `0.6.x` - Integration Hardening
2. `0.7.x` - API Freeze
3. `0.8.x` - Release Candidate
4. `1.0.0` - Stable Release

Each stage has explicit exit criteria. No stage is considered complete until all criteria pass.

## 0.6.x - Integration Hardening

### Objectives
- Confirm that argument-centric digestion works reliably across package, registry, decorator, and mixed styles.
- Validate runtime behavior with optional integrations (`beartype`, `pydantic`, `pyunitwizard`).
- Reduce ambiguity in warning behavior (`strictness`) and default configuration resolution.

### Deliverables
- End-to-end integration scenarios in tests and examples.
- Stable behavior for `_argdigest.py` auto-discovery and explicit `config=...`.
- Consistent warning/error behavior for undigested arguments.

### Exit Criteria
- Full test suite passes in a clean environment.
- No unresolved behavioral mismatches between docs and implementation for `arg_digest`.
- Smoke examples are validated in CI.

## 0.7.x - API Freeze

### Objectives
- Freeze the public API for decorators, config, errors, and pipelines.
- Remove or deprecate ambiguous naming and legacy aliases.
- Define compatibility guarantees for downstream libraries.

### Deliverables
- Public API contract document aligned with implementation.
- Clean `__all__` exports and import paths.
- Deprecation policy (if needed) with timeline and migration guidance.

### Exit Criteria
- No planned breaking changes in `arg_digest` API before `1.0.0`.
- Docs and examples use the frozen API consistently.
- Contract tests for public API symbols and behaviors pass.

## 0.8.x - Release Candidate

### Objectives
- Finalize packaging and distribution readiness for PyPI and Conda.
- Validate developer workflows (devtools, docs build, CLI flows).
- Ensure telemetry and diagnostics are stable (`smonitor` catalog integration).

### Deliverables
- Release checklist for package build, tests, docs, and CLI.
- Conda recipe validation and reproducible local build instructions.
- Final documentation pass: user guide, developer guide, API reference.

### Exit Criteria
- CI gates green for tests, linting, and documentation build.
- No blocker bugs in core digestion logic, configuration resolution, or registry execution.
- Candidate accepted for `1.0.0` with no pending breaking changes.

## 1.0.0 - Stable Release

### Objectives
- Publish a stable API and runtime behavior suitable for production integration.
- Confirm integration path for external libraries (including MolSysMT pilot scope).

### Deliverables
- Tagged `1.0.0` release.
- Final changelog and migration notes.
- Stable docs and examples for all supported digestion styles.
- Ecosystem interoperability sign-off against `devguide/1.0.0_checklist.md`.

### Exit Criteria
- Test suite and release pipeline fully green.
- API/documentation consistency verified.
- Integration sign-off completed for target downstream usage.
- Cross-layer error propagation path validated (PyUnitWizard -> ArgDigest -> SMonitor/DepDigest hints).

## Cross-Cutting Workstreams

These run throughout all stages:

- **Quality Gates**
  - `pytest` always green.
  - Linting and style checks enforced in CI.

- **Documentation Accuracy**
  - Keep README, developer guide, and docs site synchronized with runtime behavior.
  - Ensure AI-agent templates track the frozen API.

- **Observability and Diagnostics**
  - Keep catalog-based errors/warnings coherent and actionable.
  - Validate structured diagnostics for missing dependencies and missing digesters.

- **Performance**
  - Preserve import-time and runtime caching guarantees.
  - Track regressions in decorator overhead and pipeline execution path.

## Immediate Next Actions

1. Execute `1.0.0_checklist.md` sections A-E as strict release blockers.
2. Run integration confidence checks against target MolSysMT paths.
3. Keep workflow import checks strict and wheel-oriented in CI/docs pipelines.
4. Finalize release notes and migration notes for `1.0.0`.
