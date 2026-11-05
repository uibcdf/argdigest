---
summary: Qualify and publish the 0.17.1 consumer-contract and diagnostics fixes.
issue: uibcdf/argdigest#51
status: active
opened: 2026-11-05
closed:
verification: measured
area: [release, packaging, diagnostics, compatibility]
guard: tests/test_noarch_conda_publication.py
normative: devguide/conda_release_routes.md
blocked_by: []
supersedes: []
---

# Release 0.17.1

## What

Diego explicitly authorized publication of 0.17.1 after reviewing #50. Include
the confirmed attribution repair, #43–#48 source corrections and #49's public
SMonitor 0.22.1 receiving/profile. MolSysSuite release-specific notice is #169;
thematic consumer/guide coordination remains #164. Original public 0.17.0 is
immutable and #9 remains deferred.

## How

Use the committed staged noarch build-0 decision. Retain exact-candidate fast
and twelve-cell source gates, build/inspection/original upload receipts, twelve
full installed cells with public scientific fixtures and nested-signal receiving,
and twelve separate NumPy-free lower-bound cells. Only then create immutable
tag/release 0.17.1 and promote the original tested file/digest to main.

Python 3.11–3.14, Linux/macOS arm64/Windows and required runtime floors remain.
Full installed SMonitor is 0.22.1, DepDigest 0.15.1 and PyUnitWizard 0.27.0;
the separate core matrix retains SMonitor 0.16.0 / DepDigest 0.11.0.
The optional PyUnitWizard API floor is corrected to >=0.22.0. Candidate/package
identity, native runs/attempts/jobs/steps and public/archival receipts will be
appended after each actually executed boundary. No candidate file is claimed yet.

Local #50 comparison fails seven of eight new controls on exact old source;
the fixed source passes all eight, 58 focused checks and the complete 528-test
selection with three known warnings, without skips. These are source checks,
not exact-file qualification. Subsequent candidate metadata/guidance and full
hosted/installed gates retain their own checks.

## Why

Users need published fixes for literal variadic keywords, native TypeError
catch families, optional checker failures and actionable consumer diagnostics.
Packaging/backend/publisher/profile changes justify staged exact-file receiving.
Consumer scientific acceptance and byte-identical guide distribution stay with
their registered owners; a provider release does not silently update clients.
