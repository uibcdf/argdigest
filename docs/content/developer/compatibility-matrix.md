# Compatibility Matrix

This matrix defines the Python versions and the minimum sibling-library versions
validated for ArgDigest 1.0 stabilization.

## Supported Python versions

The development candidate declares `requires-python = ">=3.11,<3.15"`.
The public 0.12.1 release still supports only Python 3.11--3.13; the 3.14
claim waits for the exact candidate's full CI, staged package, public release,
and clean-install gates under `uibcdf/argdigest#13`. The bound is closed at both ends
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
