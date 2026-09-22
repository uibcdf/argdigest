---
summary: Release ArgDigest with independently verified Python 3.14 support.
issue: uibcdf/argdigest#13
status: active
opened: 2026-09-21
closed:
severity: medium
verification: measured
area: [python, compatibility, packaging, ci]
guard:
normative:
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

Next, run a non-claiming Python 3.14 feasibility matrix on hosted Linux,
macOS, and Windows with public dependencies. Only after it passes, register
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
`292c46f`; it is not yet `admitted`. Release 0.13.0 is the intended first
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
published `policy-v1.4.2`, which contains that authorization; the ArgDigest
caller is being updated. That change creates a new candidate SHA, so the
original staged build is diagnostic evidence only. The final candidate must
repeat exact-commit source, staging, and installed-package gates before
publication; build number 1 will distinguish it from the superseded staged
build 0.

## Why

Published ArgDigest 0.12.1 is restricted to Python 3.11--3.13, blocking the
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
