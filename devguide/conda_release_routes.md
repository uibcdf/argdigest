# Conda release routes

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
