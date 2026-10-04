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

## Why

Dependency resolution changes need artifact evidence before public visibility.
New digester context justifies a minor release; 1.0 remains a separate decision.

## Acceptance criteria

- Exact candidate passes source CI, suite/publication policies and docs.
- One staged noarch artifact passes full and minimal-core installed matrices.
- Numeric 0.14.0 release and identical public artifact, independently verified.
- Documentation publication and source-only Zenodo evidence tracked separately.
