# Development Notes - ArgDigest

## 2026-01-31: Refactoring and Robustness (v0.1 -> 0.2.0) ✅

- **API**: Implemented `@digest.map` and `argdigest.config`.
- **Integrations**: Native Pydantic rules and Beartype `type_check=True`.
- **Robustness**: Rich errors with context/hints and path-reporting for cycles.
- **CI/CD**: Fixed environment files and added `versioningit` support.

## Phase 3: "Batteries Included" & Science Support (0.3.0) 🚀

### 1. Standard Pipeline Library (`argdigest.pipelines`)
- Implement a set of common coercers: `to_list`, `to_bool`, `to_path`, `strip`, `lower`.
- Implement basic validators: `is_int_list`, `in_range`, `matches_regex`.
- Goal: Reduce boilerplate in user libraries.

### 2. Native PyUnitWizard Integration
- Create a `contrib.pyunitwizard` (or similar) providing pipelines for:
    - `check(dimensionality=...)`
    - `standardize()` (respecting global PUW config)
    - `convert(to_unit=...)`
- Ensure robust error handling when underlying physics libraries are missing.

### 3. MolSysMT Legacy Support
- Validate that `digestion_style="package"` correctly loads and injects dependencies for existing MolSysMT digesters.
- Ensure parameters like `caller` and `syntax` are injected seamlessly even if not explicitly defined in all functions.

### 4. Architectural Refinement
- Encourage the use of shared `kind` (e.g., `kind="vector3d"`) to compose logic between related arguments (like `coordinates` and `translation`).

---
## Next Steps
- [ ] Implement `argdigest/pipelines/base.py` with the first set of standard coercers.
- [ ] Create `argdigest/contrib/pyunitwizard.py` with initial wrappers.
- [ ] Add smoke tests using legacy-style digesters from MolSysMT.