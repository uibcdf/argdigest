---
summary: Publish 0.16.0 after exact-artifact registration-only qualification.
issue: uibcdf/argdigest#36
status: resolved
opened: 2026-10-14
closed: 2026-10-20
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

## Public qualification and reconciliation — 2026-10-20

The release was published on 2026-10-14; the queued status had not been
reconciled. Independent review now binds original source
`2b9c9b289ae9b1d97d3bf04250f5c882feab3d41`, annotated numeric tag and stable
release to `noarch/argdigest-0.16.0-py_0.tar.bz2`, SHA-256
`e82d82680d79ae3d5df9917b1662d2855ed8485128943b72ddec87a5769a467d`.
The original source/full matrix, repository/publication policies, producer,
twelve full installed cells, twelve NumPy-free lower-bound cells and same-file
promotion passed their exact required native jobs and steps on attempt 1.

Producer `38567520662`, installed matrix `38568051160`, minimal-core matrix
`38568053243` and promotion `38572471948` retain separate identities. Receipt
ZIP digests, original producer and archive coordinate/digest were checked,
including the independent actual upload receipt (the build-only action's
`upload_not_requested` is not the subsequent staging upload). Public registry,
solver index and downloaded archive agree; 38 nongenerated Python runtime
files match the original candidate.

Independent central run `39469657236` at
`b199b7e1805ed054d924b00eac8d68793e07916d` installs the same public bytes on
Linux, macOS arm64 and Windows with Python 3.14 and executes the installed
console `--help` outside source. All three exact installation/command receipts
pass. This is explicitly a console smoke check; the original twelve-cell full
installed and core matrices supply the broader release evidence.

Documentation run `38572423608` passed its installed-wheel and Sphinx steps.
Archival run `38572426093` and independent public source-archive verification
confirm source-only Zenodo record `23369539`, version DOI
`10.5281/zenodo.23369539`, concept DOI `10.5281/zenodo.22892325`. The downloaded
541,645-byte ZIP matches its published checksum; all 330 source files match
the original tagged Git tree. Package files are not claimed as Zenodo contents.

Normalized immutable identities, native jobs/steps, artifact digests and public
receipts are retained in
`devguide/evidence/release_0_16_0_public_receiving_2026-10-20.json`. The existing
`tests/test_diagnostic_registration.py` guard exercises the repaired bootstrap
mechanism in fresh processes and makes unavailable mandatory capabilities fail
qualification; it is relevant to this resolution, beyond mere addressability.

No rebuild, substitution, retagging, new upload/promotion, historical release-title
edit or scientific rerun was performed during reconciliation. Consumer
receiving remains separately owned, including Recorda #24 and Praxis #10 under
uibcdf/molsyssuite#82 / uibcdf/moli#40; publication alone does not widen a
consumer's metadata. Shared provider receiving is reported to
uibcdf/molsyssuite#106 and publication coordination to uibcdf/molsyssuite#45.
