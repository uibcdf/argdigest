---
summary: Publish 0.15.0 with scoped capture and explicit digestion after installed qualification.
issue: uibcdf/argdigest#31
status: active
opened: 2026-10-06
closed:
verification: measured
area: [release, distribution, diagnostics]
guard: tests/test_capture_policy.py
normative:
blocked_by: []
supersedes: []
---

# Release 0.15.0

## What

The maintainer authorized the numeric tag, release and published package after
the completed implementations in `uibcdf/argdigest#29`/#30. The additive public
API options justify 0.15.0. Core floors and historical inference remain unchanged.
Release coordination is `uibcdf/argdigest#31`; shared consumer impact remains
with `uibcdf/molsyssuite#106` and consumer-owned receiving decisions.

## How

Use the existing reviewed staged noarch producer/promoter and full installed
workflow pins. Build number 0 is a new coordinate. Require exact-candidate source
CI/full twelve-cell matrix and one sealed package. The full off-checkout installed
suite pins public SMonitor 0.19.0 and uses `--require-scoped-capture` so absence
cannot qualify through skipped tests. Required resources include the owning
configuration and diagnostics modules. The separate NumPy-free matrix retains
public SMonitor 0.16.0/DepDigest 0.11.0 lower bounds and checks explicit pipeline
selection and restrictive refusal in addition to existing core behavior.

SMonitor 0.19.0 is public: producer/tag `f604b940ab281df4554869fdd24f796ea6d42c27`,
`smonitor-0.19.0-py_1.tar.bz2`, SHA-256
`4b876b4993b1e2caeed40851402a931f3b245ed7c1916d9483d81bc90274e31c`.
Public promotion `37522036404` and complete installed run `37521323117` passed.
This replaces the earlier unpublished-provider limitation without claiming
ArgDigest publication or consumer adoption before their own evidence exists.

## Why

Source implementation is insufficient for releasing the opt-in capability. The
capture guard exercises zero conversions, absent payloads and native failure
preservation against the installed provider; the strict gate makes unavailable
capture a failure. Independent core evidence protects retained old-provider
compatibility. Promote the tested digest once, without rebuilding or overwriting.

## Acceptance criteria

- Exact candidate passes source CI, all twelve source cells and policies.
- One staged artifact passes full installed and minimal-core twelve-cell matrices.
- Scoped cases execute with the public provider; absence is a gate failure.
- Numeric tag, GitHub release and identical public package are independently verified.
- Public installation, documentation and source-only archival state are recorded separately.
- Source/API/canonical guide publication does not claim consumer migration.

## Local preparation evidence

The complete Python 3.14 suite passes 382 tests with
`--require-scoped-capture`; no scoped cases are skipped. An independent negative
probe using SMonitor tag source 0.16.0 fails the designated gate with its fixed
availability message rather than skipping. This local lane still uses the
maintained provider environment; public artifact qualification is the separate
hosted installed matrix. Ruff, report indexes, whitespace checks and the pinned
`43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc` dependency preflight pass. Sphinx builds
with three existing heading warnings in `docs/index.md`. A fresh all-label query
returns 404 for ArgDigest 0.15.0 before staging. Independent registry metadata
confirms SMonitor build 1 under staging/main with the published SHA-256 above.
