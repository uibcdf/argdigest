# Development Notes - ArgDigest

## 2026-01-31: Phase 3 (v0.3.0) Implementation 🚀

### 1. Standard Pipeline Library (`argdigest.pipelines`) ✅
- Implemented `coercers.py`: `to_bool`, `to_list`, `to_tuple`, `strip`, `lower`, `upper`.
- Implemented `validators.py`: `is_positive`, `is_file`, `is_dir`, `is_int`, `is_str`.
- Registered automatically via `kind="std"`.

### 2. Native PyUnitWizard Integration (`contrib/pyunitwizard_support.py`) ✅
- Implemented factories: `check(...)`, `standardize()`, `convert(...)`, `is_quantity()`.
- Verified respecting global PUW config (e.g. `set_standard_units`).
- Added robust error handling for missing libraries.

### 3. MolSysMT Legacy Support ✅
- Validated `digestion_style="package"` with argument injection.
- Confirmed that ArgDigest correctly injects dependencies (like `syntax`) into legacy digesters, passing `None` if they are missing in the call.

### 4. Documentation & Examples Updates ✅
- **README.md & DEVELOPER_GUIDE.md**: Completely modernized with new syntax and features.
- **User Guide**: Added sections for `std` pipelines and PyUnitWizard context management.
- **AI Agent Templates**: Updated all templates to include modern programmatic configuration and native integrations.
- **Examples**: Updated `packlib` to demonstrate `PUW_CONTEXT` and `type_check=True`.

### 5. Architectural Refinement
- The system is now fully capable of replacing the legacy MolSysMT digestion engine.

---
## Next Steps (v0.4.0)
- [ ] **Declarative Config**: `YAML`/`JSON` rule sets.
- [ ] **Execution Profiling**: Performance metrics.
