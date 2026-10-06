---
summary: Publish 0.15.0 with scoped capture and explicit digestion after installed qualification.
issue: uibcdf/argdigest#31
status: resolved
opened: 2026-10-06
closed: 2026-10-06
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

## Completion evidence — 2026-10-06

The original producer and annotated numeric tag `0.15.0` identify
`57447cc4ec1f7ce85078f8a939892efd075bc919`. Source CI `37523853675`, source
twelve-cell matrix `37523910657`, suite policy `37523855511`, publication policy
`37523854970` and numeric tag policy `37526673523` passed. The independent pinned
shared verifier checked actual execution of every declared scientific step,
candidate identity and attempt, separately from workflow conclusions.

Producer `37524900085`, attempt 1, sealed and staged
`noarch/argdigest-0.15.0-py_0.tar.bz2`, SHA-256
`b0f22038a8ad1c888dca10adedaca0fa14d2383a685a97c0602b7ca05f29d6a1`.
Independent inspection checked embedded version, metadata and all eight declared
resources. Full installed run `37525789576`, attempt 1, passed all twelve cells
on Linux, macOS and Windows with Python 3.11–3.14. Its complete off-checkout
scientific selection requires public SMonitor 0.19.0 and executes scoped capture
cases; every declared installation, resource, test and final provenance step
succeeded. The separate core run `37525794773`, attempt 1, passed all twelve
cells without NumPy using public SMonitor 0.16.0 `py_1` and DepDigest 0.11.0
`py_2`. The native shared verifier independently confirmed both matrices.

[GitHub Release 0.15.0](https://github.com/uibcdf/argdigest/releases/tag/0.15.0)
is public and stable, published `2026-10-06T20:28:47Z`. Release-triggered producer
`37526754834` verified the staged decision and skipped its direct publish job.
Promotion `37526759902`, attempt 1, passed the public-release/core guard, full
installed verifier, same-file promotion and public registry/solver checks. Its
`noarch-promotion-37526759902-1` receipts identify the original SHA-256 and
`main` label. An independent read-only probe again confirmed both public metadata
and the solver-visible hash. No rebuild, overwrite or retag was performed.

A fresh Linux Python 3.14.8 environment solved
`uibcdf::argdigest=0.15.0=py_0` and `uibcdf::smonitor=0.19.0=py_1` exclusively
from public UIBCDF/Conda-forge channels. DepDigest resolved to public 0.13.0.
The downloaded Conda archive matched the producer digest; all eight required
installed files matched its bytes. Runtime imports resolved inside the fresh
prefix. NumPy remained absent, the CLI succeeded and `pip check` found no broken
requirements. Digester and pipeline failure probes made zero argument/exception
conversions, omitted payloads and preserved native exception identity and cause.
Explicit `argument_digestion=False` retained pipeline execution and rejection of
unknown arguments with `DigestConfig` present.

Documentation run `37526753843` passed. Public
[release notes](https://www.uibcdf.org/argdigest/content/about/release-notes.html)
and [SMonitor guidance](https://www.uibcdf.org/argdigest/content/user/smonitor.html)
expose 0.15.0 and the public SMonitor 0.19.0 availability requirement.

Zenodo workflow `37526754578` explicitly verified source-only record `23197285`,
version DOI [10.5281/zenodo.23197285](https://doi.org/10.5281/zenodo.23197285),
under concept DOI `10.5281/zenodo.22892325`. Independent download verified the
508483-byte ZIP, MD5 `b17f9bdc6b22ec50e4a7aeb0aad4c1ba`, SHA-256
`d372310ec9edbcc45f9fb32e94f623b2d787dc7c7139891dde99c8bfa1e83147`.
All 318 archived file blobs matched the original tagged Git tree. This evidence
covers the source snapshot; the Conda artifact has its separate receipt.

Durable structured evidence: `../evidence/release_0_15_0_2026-10-06.json`.
The selected capture guard asserts zero conversions, absent payloads and native
failure preservation; the installed gate's strict availability option prevents
missing-provider skips from qualifying the new public capability. Core release
guards separately reject incomplete or unexecuted matrix evidence before
promotion. Consumer-specific adoption remains with `uibcdf/molsyssuite#106`
and receiving owners; provider publication does not qualify sibling consumers.
