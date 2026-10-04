---
summary: Publish 0.14.0 after exact-source and staged installed qualification.
issue: uibcdf/argdigest#24
status: open
opened: 2026-10-04
closed:
severity: medium
verification: asserted
area: [release, distribution]
guard:
normative:
blocked_by: [uibcdf/molsyssuite#99]
supersedes: []
---

# Release 0.14.0

## What

Release the optional NumPy boundary, lazy PyUnitWizard loading, corrected bypass
and classmethod behavior, richer refusals and optional runtime `qualname`.
The maintainer authorized publication on 2026-10-04. Consumer coordination is
`uibcdf/molsyssuite#98`.

## How

The committed staged decision and resource inventory use shared noarch workflows
at `5090a656cd8223826947575f329ee52aa664c725`. Require executed source tests,
full installed tests outside source, and a separate minimal-core lower-bound
matrix. Promote the validated digest only after the public release exists.
Zenodo uses bounded probes and six-hour recovery with a fixed adoption date.

The off-checkout wheel rehearsal found four administrative failures: the API
reference test used a relative working-directory path, and the reporting tests
could import a sibling `devtools.devguide_reports`. Resolve maintained evidence
from the test file and load the owning script by its exact path. These corrections
preserve the complete installed selection and keep ArgDigest runtime imports
outside source.

Staging attempt `37209744706` failed before upload because the migrated recipe
declared `build.script` alongside the existing `build.sh`. Both upload steps
were skipped. Keep `build.sh` as the sole installer and remove its old version
freezing call: the shared publisher already freezes the reviewed version in the
ephemeral checkout. No artifact coordinate was occupied by this attempt; build 0
remains available. Requalify the new producer candidate before retrying staging.

Producer `37210475369` successfully staged the immutable original candidate
`0fa776af2d271065c60727c28480b20c3ce09aee` as
`argdigest-0.14.0-py_0.tar.bz2`, SHA-256
`983dca0f6bd0944d81fb1efc01e1dfa5c951e95abac6e7a0a08a13b7370d3b9e`.
Minimal-core run `37211211381` passed all twelve cells without NumPy, with the
public DepDigest 0.11.0 and SMonitor 0.16.0 lower-bound builds.

Full installed run `37211210817` passed Linux and macOS, but Windows failed
before installing ArgDigest: the shared provider's Python subprocess could not
resolve its Conda batch entry (`WinError 2`). The provider owns the repair in
`uibcdf/molsyssuite#99`. The installed caller pins proposed provider commit
`13a661e348275496a677a1bfe9650d68a03713a3` for hosted qualification; provider
owner review is pending. The promoter accepts a separate administrative
`qualification_sha`, preserving the original producer SHA, package, plan,
complete scientific test selection and digest. Do not rebuild the occupied
coordinate or move the eventual numeric tag away from the original producer.

## Why

Dependency resolution changes need artifact evidence before public visibility.
New digester context justifies a minor release; 1.0 remains a separate decision.

## Acceptance criteria

- Exact candidate passes source CI, suite/publication policies and docs.
- One staged noarch artifact passes full and minimal-core installed matrices.
- Numeric 0.14.0 release and identical public artifact, independently verified.
- Documentation publication and source-only Zenodo evidence tracked separately.
