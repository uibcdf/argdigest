# Compatibility Matrix

This matrix defines the Python versions and the minimum sibling-library versions
validated for ArgDigest 1.0 stabilization.

## Supported Python versions

ArgDigest declares `requires-python = ">=3.11,<3.14"`. The bound is closed at both ends
on purpose: the lower end is the oldest version the test suite can run on, and the upper
end is the newest version actually exercised. An open upper bound would promise support
for a Python that has never been tested against.

| Python | Ubuntu | macOS |
|---|---|---|
| `3.11` | tested | tested |
| `3.12` | tested | tested |
| `3.13` | tested | tested |

Every cell is a job in `.github/workflows/CI_full_matrix.yaml`. The per-push gate
(`.github/workflows/CI.yaml`) runs one cell of it — Ubuntu on `3.13` — so a pull request
gets a fast answer; the full six-cell matrix runs weekly and on demand.

## Sibling libraries

| Component | Minimum Version | Role |
|---|---:|---|
| `smonitor` | `0.11.4` | diagnostics, signaling, catalog-backed messaging |
| `depdigest` | `0.9.1` | optional dependency routing and hints |
| `pyunitwizard` | `0.11.0` | optional unit-aware pipelines (`argdigest[pyunitwizard]`) |

## Notes

- `smonitor` and `depdigest` are hard runtime dependencies for ArgDigest core.
- `pyunitwizard` is optional and required only when using quantity pipelines.
- Compatibility is validated in CI and release checklists. Any matrix change
  requires updating docs, tests, and release notes together.
- `tests/test_compatibility_matrix.py` holds this page, `pyproject.toml`, and the CI
  workflows to the same numbers, so the three cannot drift apart silently.
