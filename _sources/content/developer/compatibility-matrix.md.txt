# Compatibility Matrix

This matrix defines the Python versions and the minimum sibling-library versions
validated for ArgDigest 1.0 stabilization.

## Supported Python versions

Public release 0.13.0 declares `requires-python = ">=3.11,<3.15"` and supports
Python 3.11--3.14. The exact source and staged installed-package matrices both
passed all twelve Linux, macOS, and Windows cells under `uibcdf/argdigest#13`;
the same staged file was promoted to the public `uibcdf` channel. The bound is closed at both ends
on purpose: the lower end is the oldest version the test suite can run on, and the upper
end is the newest version actually exercised. An open upper bound would promise support
for a Python that has never been tested against.

| Python | Ubuntu | macOS | Windows |
|---|---|---|---|
| `3.11` | required | required | required |
| `3.12` | required | required | required |
| `3.13` | required | required | required |
| `3.14` | required | required | required |

Every required cell is a job in `.github/workflows/CI_full_matrix.yaml`. The per-push gate
(`.github/workflows/CI.yaml`) runs one cell of it — Ubuntu on `3.13` — so a pull request
gets a fast answer; the full twelve-cell matrix runs weekly and on demand. The
3.14 and Windows cells exercise the core with public SMonitor and DepDigest;
optional PyUnitWizard tests are omitted there until its own 3.14 transition.
The 0.13.0 source matrix is run `35695504353`; the installed-package matrix
is run `35696336418`. The public `noarch` file is
`argdigest-0.13.0-py_1.tar.bz2`.

## Sibling libraries

| Component | Minimum Version | Role |
|---|---:|---|
| `smonitor` | `0.16.0` | diagnostics, signaling, catalog-backed messaging |
| `depdigest` | `0.11.0` | optional dependency routing and hints |
| `pyunitwizard` | `0.11.0` | optional unit-aware pipelines (`argdigest[pyunitwizard]`) |

## Notes

- `smonitor` and `depdigest` are hard runtime dependencies for ArgDigest core.
- `pyunitwizard` is optional and required only when using quantity pipelines.
- Compatibility is validated in CI and release checklists. Any matrix change
  requires updating docs, tests, and release notes together.
- `tests/test_compatibility_matrix.py` holds this page, `pyproject.toml`, and the CI
  workflows to the same numbers, so the three cannot drift apart silently.
