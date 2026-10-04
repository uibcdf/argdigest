---
summary: Publish 0.14.0 after exact-source and staged installed qualification.
issue: uibcdf/argdigest#24
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: measured
area: [release, distribution]
guard: tests/test_core_release_gate.py::test_core_gate_rejects_incomplete_or_unexecuted_evidence
normative:
blocked_by: []
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
`uibcdf/molsyssuite#99`. The installed caller pins provider commit
`13a661e348275496a677a1bfe9650d68a03713a3` for hosted qualification. The maintainer
approved its owner review on 2026-10-04; `uibcdf/molsyssuite#100` merged as
`d2ae65d3caba78420c9391213faab1964a8164ce`. The promoter accepts a separate administrative
`qualification_sha`, preserving the original producer SHA, package, plan,
complete scientific test selection and digest. Do not rebuild the occupied
coordinate or move the eventual numeric tag away from the original producer.

## Completion evidence — 2026-10-04

- Original producer and numeric tag `0.14.0` identify
  `0fa776af2d271065c60727c28480b20c3ce09aee`. Source CI `37210300854`,
  source twelve-cell suite `37210325527`, suite policy `37210301221` and
  publication policy `37210301182` passed.
- Installed twelve-cell run `37213239915`, attempt 1, passed on Linux, macOS
  and Windows with Python 3.11–3.14. Every declared install, resource validation,
  scientific-test and final provenance step actually succeeded. Its sealed
  source binding identifies administrative qualification commit
  `be39e899f3b9fef2d4ce705799ae19770f41f769` and the unchanged original producer
  and digest. The independent shared verifier confirmed all native cells and
  steps. Minimal-core run `37211211381` independently passed all twelve cells
  without NumPy and with public DepDigest 0.11.0 `py_2` and SMonitor 0.16.0 `py_1`.
- [GitHub Release 0.14.0](https://github.com/uibcdf/argdigest/releases/tag/0.14.0)
  is public, stable, release ID `403093400`, published `2026-10-04T15:57:56Z`.
  The annotated tag resolves to the original producer. Release-triggered run
  `37214985408` verified its route and skipped the build/upload job.
- Promotion `37215001335`, attempt 1, passed the public-release/core guard,
  existing full-installed verifier, same-file label promotion, independent
  public registry/index verification and receipt retention. Receipt artifact
  `noarch-promotion-37215001335-1` has GitHub digest
  `sha256:576c7bc90d5583e90920a7c1a12a8b0df0cace0737d0c9978e6e8a0f5ef0989a`.
  Independent read-only inspection confirmed the same package SHA-256 under
  labels `staging` and `main`, visible in the public solver index.
- A fresh Linux Python 3.14.7 environment solved
  `uibcdf::argdigest=0.14.0=py_0` using public UIBCDF/Conda-forge channels.
  The downloaded archive matches the producer SHA-256; all six required
  installed resources match its bytes. Imports resolve inside that prefix,
  package/metadata versions are 0.14.0, CLI succeeds, and `pip check` reports
  no broken requirements. NumPy remains absent; the installed core probe passes
  science-remedy, classmethod, runtime-qualname and literal-True bypass checks.
- Documentation workflow `37214985039` passed; the public
  [release notes](https://www.uibcdf.org/argdigest/content/about/release-notes.html)
  contain 0.14.0 and its migration guidance.
- Zenodo exact-tag probe and hosted archival workflow `37214985721` verified
  source-only record `23139769`, version DOI
  [10.5281/zenodo.23139769](https://doi.org/10.5281/zenodo.23139769), concept DOI
  `10.5281/zenodo.22892325`. Downloaded source ZIP is 473066 bytes, MD5
  `53deac7a761c90d9b9b98faf13ad3c0d`, SHA-256
  `ade9e8a7fd3c7b39a2d498bf4e04a93ac0fdd56431b4aaf875d3d6888e35787e`.
  All 309 archived file blobs match the original tagged Git tree. This does
  not claim Conda-package archival.

The guard rejects incomplete/skipped/duplicate matrix cells or unexecuted steps,
wrong source/hash identity and attempt mismatches before promotion. Shared
installed-matrix verification separately protects the full scientific suite.
MolSysSuite consumer receiving review/adoption/deferral remains owned by
`uibcdf/molsyssuite#98`; no sibling scientific acceptance is inferred from this
provider release.

## Why

Dependency resolution changes need artifact evidence before public visibility.
New digester context justifies a minor release; 1.0 remains a separate decision.

## Acceptance criteria

- Exact candidate passes source CI, suite/publication policies and docs.
- One staged noarch artifact passes full and minimal-core installed matrices.
- Numeric 0.14.0 release and identical public artifact, independently verified.
- Documentation publication and source-only Zenodo evidence tracked separately.
