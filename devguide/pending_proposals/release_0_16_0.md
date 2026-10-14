---
summary: Publish 0.16.0 after exact-artifact registration-only qualification.
issue: uibcdf/argdigest#36
status: active
opened: 2026-10-14
closed:
verification: inspected
area: [release, distribution, diagnostics]
guard: tests/test_diagnostic_registration.py
normative:
blocked_by: []
supersedes: []
---

# Release 0.16.0

## What

The maintainer authorized publication on 2026-10-14 after the source review of
`uibcdf/argdigest#32`. Registration-only diagnostics and explicit configuration
helpers are additive public APIs that justify 0.16.0. Python 3.11–3.14 and the
SMonitor 0.16.0 / DepDigest 0.11.0 core floors remain unchanged.

## How

Use the existing pinned staged noarch producer and promoter, build number 0.
Require exact-candidate CI, all twelve source cells and policies. Build once;
record the original candidate, producer, filename and sealed digest. Run all
twelve full off-checkout installed cells using public SMonitor 0.21.0 and
DepDigest 0.15.1, requiring both registration-only and scoped-capture cases.
Run all twelve separate NumPy-free core cells with the retained lower bounds,
including explicit refusal of unavailable registration-only diagnostics.

After qualification, publish the numeric tag and stable GitHub release and
promote the same tested file. Independently check public registry/solver state,
fresh installation, documentation and source-only Zenodo archival. Preserve
normalized receipts and archive this report and #32 with their issue outcomes.

## Why

Source implementation and a private wheel do not qualify a public artifact.
`tests/test_diagnostic_registration.py` protects application policy, handlers,
hooks and original exceptions and proves the installed profile cannot pass by
skipping an unavailable registration capability. Independent lower-bound core
evidence protects legacy compatibility. Consumer receiving remains independently
owned; shared coordination is `uibcdf/molsyssuite#106`.

## Acceptance criteria

- Exact candidate passes CI, all twelve source cells and policies.
- One sealed artifact passes both complete twelve-cell installed matrices.
- Registration-only and scoped-capture cases execute with public providers.
- Public tag, release and identical package are independently checked.
- Public installation, docs and source-only archival have separate receipts.
- Reports/indexes and owning GitHub issues agree at closure.

## Preparation

Prerelease source/profile review is recorded in
`evidence/registration_only_final_review_2026-10-14.json`. Those local results
are preparation evidence; they do not replace this release's exact gates.
Only #32 and explicitly post-1.0 #9 were open before filing this release issue;
there were no open pull requests.
