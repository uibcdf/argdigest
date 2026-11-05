# Compatibility Matrix

This matrix separates declared API floors from executed compatibility evidence.
Receiving a guide or resolving dependencies does not qualify an untested combination.

## Supported Python versions

Current macOS support is limited to Apple Silicon (arm64). Intel macOS is
outside the supported matrix; concrete user demand may reopen
[the suite decision](https://github.com/uibcdf/molsyssuite/issues/59).
Previously recorded release evidence keeps its original scope.

Public release 0.17.0 declares `requires-python = ">=3.11,<3.15"` and supports
Python 3.11--3.14. All twelve source, full installed and separate minimal-core
cells passed before same-file public promotion under `uibcdf/argdigest#40`.
The Python range follows the separately governed suite policy.

| Python | Ubuntu | macOS | Windows |
|---|---|---|---|
| `3.11` | required | required | required |
| `3.12` | required | required | required |
| `3.13` | required | required | required |
| `3.14` | required | required | required |

Every required cell is a job in `.github/workflows/CI_full_matrix.yaml`. The
per-push gate (`.github/workflows/CI.yaml`) runs Ubuntu on `3.14`; full matrices
run weekly, on recovery and on demand. The source profiles include scientific
fixtures on every platform/minor. The separate installed-core matrix omits NumPy.
0.17.0 used source run `39878899217`, full installed `39879578589` with public
SMonitor 0.21.0 / DepDigest 0.15.1 / PyUnitWizard 0.27.0, and core `39879578248`
with SMonitor 0.16.0 / DepDigest 0.11.0. Historical receipts remain in the
archived release reports; development changes require their own next candidate.

## Sibling libraries

| Component | Minimum Version | Role |
|---|---:|---|
| `smonitor` | `0.16.0` | diagnostics, signaling, catalog-backed messaging |
| `depdigest` | `0.11.0` | optional dependency routing and hints |
| `pyunitwizard` | `0.22.0` | optional unit-aware pipelines (`argdigest[pyunitwizard]`; development after 0.17.0) |

The PyUnitWizard API minimum is corrected after 0.17.0: `context` is exported
from 0.18.0, and the consumed `fast_track` canonical converters from 0.22.0.
0.11.0 does not provide these APIs. This floor is based on tagged provider
source inspection; it is not a new twelve-cell installed-floor qualification.
0.17.0's immutable metadata still declares the earlier floor.

Other optional API floors remain NumPy 1.20 (`asarray`, dtypes and arrays),
Pandas 2.0 (`DataFrame`), Pydantic 2.0 (`model_validate`), Beartype 0.16
(`beartype`) and PyYAML 6.0 (`safe_load`). Solvers must also select builds
compatible with the requested Python. Exact test/release fixtures retain their
own reproducibility pins; unexecuted minima/newer versions are not certified.

## Notes

- `smonitor` and `depdigest` are hard runtime dependencies for ArgDigest core.
- `pyunitwizard` is optional and required only when using quantity pipelines.
- Compatibility is validated in CI and release checklists. Any matrix change
  requires updating docs, tests, and release notes together.
- `tests/test_compatibility_matrix.py` holds this page, `pyproject.toml`, and the CI
  workflows to the same numbers, so the three cannot drift apart silently.
