---
summary: Adopt SPDX metadata with tested compatible build backend routes.
issue: uibcdf/argdigest#44
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: measured
area: [packaging, licensing]
guard: tests/test_noarch_conda_publication.py::test_modern_license_backend_floor_matches_all_build_routes
normative:
blocked_by: []
supersedes: []
---

# License and build metadata review

## What

Review under uibcdf/molsyssuite#162. The original MIT license and copyright/notice
bytes are preserved. This changes source metadata, not the license or old public bytes.

## How

Use SPDX `license = "MIT"` and explicit `license-files = ["LICENSE"]`.
Setuptools >=77.0.3 is aligned across build-system requirements, Conda host and
the no-build-isolation build environment. Retain the versioningit~=3 build plugin
range and Python/platform scope. No deprecated license classifier was present.
The minimum was selected for PEP 639 support and its early handling corrections.

Real Python 3.14.7 no-isolation builds use both Setuptools 77.0.3 and 84.0.0,
with versioningit 3.3.0 and build 1.6.1. Each creates an sdist and a wheel rebuilt
from that sdist. Metadata advertises License-Expression MIT and License-File
LICENSE; actual notice bytes match the source in both sdists and rebuilt wheels.
Receipts retain tool versions and hashes. The permanent guard prevents pre-feature
SPDX backend floors or weaker Conda/build-environment requirements.

## Why

Backend and notice delivery are verified rather than inferred from source fields.
The plugin's absolute earliest version, other interpreters/platforms and a future
Conda artifact were not newly qualified. Existing 0.17.0 tags/files stay immutable;
these source declarations enter a future normal release candidate.
