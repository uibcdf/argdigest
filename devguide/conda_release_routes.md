# Conda release routes

## Current route from 0.14.0

Release ownership: `uibcdf/argdigest#24`; consumer notice:
`uibcdf/molsyssuite#98`. The reviewed plan and resource inventory now use the
shared producer, promoter and archival workflows at
`5090a656cd8223826947575f329ee52aa664c725`. Installed qualification pins
`13a661e348275496a677a1bfe9650d68a03713a3`, the accepted native Windows Conda
repair in `uibcdf/molsyssuite#99` / `uibcdf/molsyssuite#100`.
This adopts the qualified build/upload repairs without requesting the deferred
general provider v2.3.0 rollout.

The build checks every declared source job and test step, builds once, inspects
embedded metadata/resources, then seals and uploads the exact file. The full
installed workflow runs all `tests/` outside source with public scientific
dependencies and checks provenance before/after. A separate twelve-cell
minimal-core matrix checks public dependency lower bounds without NumPy and
exercises classmethods, runtime `qualname` and literal-True bypass behavior.
Both matrices must pass before promotion. The promoter binds the full installed
run, verifies the public GitHub release and minimal-core matrix, then adds the
main label to the same SHA-256 and independently checks registry and solver index.

Use the committed build number. Package repairs require a new candidate and
additive build number. Administrative workflow repairs can qualify the unchanged
artifact under a separate full `qualification_sha`; preserve the original
producer, scientific selection, file digest and numeric tag. Never retry an
uncertain upload or promotion. Read-only public
verification may be repeated independently. Zenodo uses the pinned resumable
workflow, exact-tag manual probes and six-hour discovery from the fixed
2026-10-04 adoption cutoff. Pending ingestion is not an archival claim.

Public 0.14.0 is `argdigest-0.14.0-py_0.tar.bz2`, SHA-256
`983dca0f6bd0944d81fb1efc01e1dfa5c951e95abac6e7a0a08a13b7370d3b9e`.
The producer/tag identify `0fa776af2d271065c60727c28480b20c3ce09aee`;
installed workflow qualification identifies
`be39e899f3b9fef2d4ce705799ae19770f41f769`. Full installed run `37213239915`
and minimal-core run `37211211381` passed all twelve cells each. Promotion run
`37215001335` published the same digest; fresh public installation and source-only
Zenodo record `23139769` were independently verified. Complete receipts:
`completed_proposals/release_0_14_0.md`.

## Historical local route through 0.13.0

ArgDigest follows the two-route contract being developed in
`uibcdf/molsyssuite#27`. Before tagging, the committed
`devtools/conda-build/release_plan.toml` names one canonical version, direct or
staged route, reason, decision owner, and required exact-commit workflows.
The workflow checks that plan and GitHub's successful runs at the candidate
SHA. A package coordinate never denotes two byte sequences; never use
`--force` to repair a build.

The direct route is for a release with no pre-public installed-package gate or
staged file. It requires an empty version across the registry before building,
testing, and uploading to `main` once. The staged route is required when Python
or platform support, package topology, or dependency resolution needs installed
verification before public visibility. It uploads one `noarch: python` file to
`uibcdf/label/staging`, tests the exact file off-checkout, then promotes its
existing digest to `main` after a public GitHub Release. A higher build number
supersedes a defective staged candidate without overwriting it.
For a staged release, the release-triggered workflow validates the exact plan
and gates but deliberately skips the direct build; the explicit promotion
workflow performs publication. This avoids a misleading red direct-route job
without silently rebuilding a staged coordinate.

GH Run Receptor is the first inspection path for CI and Conda runs. Its compact
report is not registry evidence: retain exact GitHub run conclusions, producer
and route receipts, Anaconda file name/SHA-256 records, public package
installation, and Zenodo source-archive verification separately. The public
Python badge and central `admitted` state change only after those gates pass.

The 0.13.0 plan selected `staged`. Candidate commit
`9880fa7b990fd0987ff0de715b665eb9e11c11b2` passed the 12-cell source
matrix (`35695504353`) and policy gate (`35695504851`). Staging producer run
`35695683898` created `argdigest-0.13.0-py_1.tar.bz2`; run `35696336418`
verified its receipts and twelve clean installations. GitHub Release 0.13.0
is public, and release run `35697325021` skipped rebuilding. Promotion run
`35697373110` moved the same file to `uibcdf/noarch`. Independent public
registry inspection matched SHA-256
`273ae5053d0aaa2d207ec9a2c684588fe3da539219b1d91cdea3b1f8dd265007`.
A fresh Linux Python 3.14.7 environment installed `argdigest=0.13.0=py_1`
from public `uibcdf` and `conda-forge`, imported the package off-checkout,
and ran its CLI. Zenodo record `22892326` verified the source snapshot only;
it does not claim Conda archival.
