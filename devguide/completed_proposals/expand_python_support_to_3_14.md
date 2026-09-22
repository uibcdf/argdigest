---
summary: Release ArgDigest with independently verified Python 3.14 support.
issue: uibcdf/argdigest#13
status: resolved
opened: 2026-09-21
closed: 2026-09-22
severity: medium
verification: measured
area: [python, compatibility, packaging, ci]
guard: tests/test_compatibility_matrix.py::test_readme_badge_lists_the_supported_pythons
normative: devguide/conda_release_routes.md
blocked_by: []
supersedes: []
---

# Expand ArgDigest support to Python 3.14

## What

Deliver a public ArgDigest release supporting Python 3.14 under
`uibcdf/molsyssuite#29`. This is a component-specific transition; neither a
source checkout nor another component's admission authorizes a public claim.

## How

The first Linux feasibility environment resolved public DepDigest 0.11.0 build
`py_2` and SMonitor 0.16.0 build `py_1` with Python 3.14.7. From this source
checkout, 224 tests passed using 12 workers; seven optional PyUnitWizard tests
were skipped because PyUnitWizard was not installed. Pint was included for the
cross-repository source E2E test. Two pre-existing testability defects were
exposed: an optional PyUnitWizard import left the test-mockable `puw` name
undefined, and the compatibility test expected an obsolete badge color. Both
were corrected locally before this measurement. This is source feasibility,
not installed-package or hosted-platform evidence.

The first hosted feasibility run `35668425976` failed identically on all three
platforms because a clean checkout lacks the generated `argdigest/_version.py`
that existed in the local development checkout. The workflow must install the
editable development source with `--ignore-requires-python` while the declared
upper bound is still 3.14. That is intentionally not a public support claim.

The agreed sequence was to run a non-claiming Python 3.14 feasibility matrix on hosted Linux,
macOS, and Windows with public dependencies. Only after it passed, register
ArgDigest as `authorized` in the central transition and update metadata,
CI, Conda recipe, tests, docs, and release notes together. Stage an exact
commit and file; run the full source matrix, clean installed-package matrix,
and consumer checks before promoting the same bytes. Independently verify
the public Conda coordinate and required Zenodo source archive before central
`admitted` status.

The corrected hosted run `35668756549` passed all three platforms at commit
`4fdbf19d386bbf476455d35c9988bf00624873e1`. GH Run Receptor reported
3/3 passing jobs, and GitHub independently confirmed that SHA and each job
conclusion. MolSysSuite registered ArgDigest as `authorized` in commit
`292c46f`; it was not yet `admitted` at that point. Release 0.13.0 became the first
candidate. The committed release plan selects the staged route because both
the support range and Conda package topology change.

The complete hosted source matrix passed 12/12 jobs on Linux, macOS, and
Windows with Python 3.11--3.14 at commit
`751d4087e8ff50f3249bef2e3405366907adc8a0` (run `35693030023`).
The first staging attempt (`35694025305`) stopped before building because its
GitHub run-list query did not yet return that successful run; the same gate
subsequently passed locally. Repeating the workflow produced the noarch
`argdigest-0.13.0-py_0.tar.bz2` in `uibcdf/label/staging` (run `35694350694`).
Producer receipts and 12 clean installed-package cells passed in run
`35694760523`, including Python 3.14 on all three platforms. This is staged
evidence, not public support.

The policy gate on the original candidate failed because immutable
`policy-v1.4.1` predates ArgDigest's central authorization. MolSysSuite
published `policy-v1.4.2`, which contains that authorization. That change
created a new candidate SHA, so the original staged build is diagnostic
evidence only. Build number 1 distinguished the final staged artifact from
the superseded build 0.

The final commit `9880fa7b990fd0987ff0de715b665eb9e11c11b2` passed the
12-cell source matrix (`35695504353`) and policy gate (`35695504851`).
Staging run `35695683898` produced noarch build `py_1`; run `35696336418`
verified its producer receipts and twelve clean installed-package cells.
GitHub Release `0.13.0` is public. Its release-triggered workflow
`35697325021` checked the staged route and skipped rebuilding. Promotion run
`35697373110` moved the exact file to `uibcdf/noarch`; the independent public
channel query matched SHA-256
`273ae5053d0aaa2d207ec9a2c684588fe3da539219b1d91cdea3b1f8dd265007`.
A clean public-channel Linux Python 3.14.7 environment installed ArgDigest
0.13.0, DepDigest 0.11.0, and SMonitor 0.16.0, imported them outside the
checkout, and ran the ArgDigest CLI. Zenodo record `22892326` confirms the
public 0.13.0 source snapshot, concept DOI `10.5281/zenodo.22892325`, and
version DOI `10.5281/zenodo.22892326`. The central public audit verified its
file name, size, and checksum. The archive covers source, not Conda bytes.
MolSysSuite admitted ArgDigest under `uibcdf/molsyssuite#29` and published
policy `1.4.3` to authorize the updated Python badge.

## Why

At opening, published ArgDigest 0.12.1 was restricted to Python 3.11--3.13, blocking the
next members of the dependency chain on Python 3.14. The now-public noarch
DepDigest and SMonitor packages remove the hard-runtime dependency boundary,
but ArgDigest must prove its own behavior and package delivery.

## Acceptance criteria

- Hosted, non-claiming 3.14 source feasibility passes on Linux, macOS, Windows.
- Central `authorized` state precedes the target-range metadata change.
- Metadata, tests, CI, recipe, compatibility docs, and release notes agree.
- A staged exact-file artifact passes clean installed-package tests on 3.11--3.14.
- A GitHub Release, exact-file public Conda promotion, clean public installs,
  and independently verified Zenodo record precede central `admitted` status.
