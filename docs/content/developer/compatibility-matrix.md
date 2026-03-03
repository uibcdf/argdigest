# Compatibility Matrix

This matrix defines the minimum sibling-library versions validated for ArgDigest
1.0 stabilization.

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
