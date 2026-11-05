---
summary: Review and align required and optional runtime API floors.
issue: uibcdf/argdigest#43
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: inspected
area: [dependencies, compatibility]
guard: tests/test_compatibility_matrix.py
normative:
blocked_by: []
supersedes: []
---

# Runtime dependency bounds review

## What

Owner audit of pyproject required/optional dependencies, recipe runtime/host,
all five environment roles, maintained acquisition routes and exact qualification
fixtures under uibcdf/molsyssuite#137. Baseline source is 615cdf4.

## How

Required core floors remain SMonitor >=0.16.0 (signal, catalog integration and
legacy setup) and DepDigest >=0.11.0 (dependency checking and availability).
Their NumPy-free twelve-cell installed lower bounds were qualified in 0.17.0;
new scoped/registration features retain explicit capability checks. No cap is
added for an untested next minor.

The optional PyUnitWizard >=0.11.0 floor was insufficient: tagged 0.11.0 exports
neither context nor fast_track; context first appears at 0.18.0 and the consumed
fast_track converters at 0.22.0. Both extras now require >=0.22.0, based on
inspection of the actual tagged exports/api/specialized source. This does not
claim a new installed floor matrix. Existing full scientific fixtures retain
public 0.27.0; local source tests use the actual shared development providers.

Other optional floors are retained for consumed APIs: NumPy >=1.20.0 arrays,
asarray/dtypes; Pandas >=2 DataFrame; Pydantic >=2 model_validate; Beartype >=0.16
beartype; PyYAML >=6 safe_load. Runtime-bearing environments now preserve these
minima wherever those optional packages are present. Exact PyUnitWizard 0.27.0
and installed-test numpy/pandas bounds remain reproducibility fixture choices,
not production caps. Python >=3.11,<3.15 is separately governed; versioningit~=3
is a build-plugin constraint. Recipe runtime stays core-only. No source sibling
acquisition route is added. Dependency preflight passes and a cross-input guard
protects present optional floors as well as existing core checks.

## Why

The maintained compatibility page now separates declared API minima from executed
installed/public evidence and corrects stale 0.13/3.13/science-skip wording.
Unknown versions/all optional-minimum platforms are not certified by this audit.
Next release qualification retains its exact-source/artifact/provider gates.
