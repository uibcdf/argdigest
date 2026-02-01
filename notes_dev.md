# Development Notes - ArgDigest

## 2026-01-31: Phase 3 (v0.3.0) Implementation ✅
- **Standard Pipelines**: Built-in coercers and validators.
- **Science Integration**: Deep PyUnitWizard support with context management.
- **Legacy Support**: Full compatibility with MolSysMT package-style digesters.
- **Documentation**: Overhauled README, Developer Guide, and AI Templates.

## Phase 4: Declarative & Data-Aware (0.4.0) 🚀

### 1. Declarative Configuration (YAML / JSON)
- Enable loading rules and configuration from external files.
- Implement `argdigest.config.load_from_file()`.
- Objective: Separation of validation logic from Python code.

### 2. Data Science Pipelines (Numpy / Pandas)
- Specialized validators for shapes, ndim, and dtypes.
- Coercers for structured data (e.g., `to_numpy`).

### 3. Advanced Auditing & Profiling
- Performance metrics for pipeline execution.
- Audit reports for deep debugging.

### 4. DevOps Automation
- Automated publishing to PyPI and Conda-forge.
- Reach 90% test coverage.

---
## Next Steps
- [ ] Add `PyYAML` as an optional dependency.
- [ ] Implement YAML/JSON parsing logic in `core/config.py`.
- [ ] Create initial Numpy-based pipelines in `pipelines/data.py`.