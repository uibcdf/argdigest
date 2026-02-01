# Development Notes - ArgDigest

## 2026-01-31: Phase 4 (v0.4.0) Implementation ✅
- **Declarative Config**: Support for YAML/JSON files.
- **Data Science**: Numpy and Pandas specialized pipelines.
- **Performance**: Execution profiling and audit logs.
- **Quality**: Reached 90% coverage and configured Codecov.

## Phase 5: Performance & Real-world (0.5.0) 🚀

### 1. Digestion Plan Caching (Extreme Performance)
- Analyze function signature and digesters once at decoration time.
- Generate a static "Execution Plan".
- Minimize runtime overhead during function calls.

### 2. CLI Audit Tool (`argdigest audit`)
- Utility to inspect validation rules in Python files/packages.
- Generate reports of applied rules per function.

### 3. Release Automation (CI/CD Final)
- Auto-publish to PyPI and Conda-forge on GitHub release.

### 4. MolSysMT Integration (Final Step)
- Migrate key modules of MolSysMT to use ArgDigest.

---
## Next Steps
- [ ] Implement `DigestionPlan` class in `core/decorator.py`.
- [ ] Refactor `@digest` to pre-calculate the plan.
- [ ] Benchmark before/after caching.
