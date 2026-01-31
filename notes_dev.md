# Development Notes - ArgDigest

## 2026-01-31: Refactoring and Robustness (v0.1 -> v0.2 transition)

### 1. API Enhancements
- **Implemented `@digest.map(...)` alias**: Now allows cleaner syntax for per-argument configuration using keyword arguments.
- **Improved `@digest(kind="...", rules=[...])`**: Fixed a bug where global kind/rules were ignored if `map` was not provided. Now they apply to all function arguments by default.

### 2. Error Handling & Transparency
- **Rich Exception Context**: `DigestError` and its subclasses now carry a `Context` (or `SimpleNamespace`) object. The string representation now includes function name, argument name, value (truncated), and hints.
- **Full Dependency Cycle Reporting**: When a cyclic dependency is detected during argument-centric digestion, the error message now displays the full path (e.g., `a -> b -> a`).

### 3. Logging System
- **Centralized Logger**: Created `argdigest/core/logger.py` with a configurable "argdigest" logger.
- **Traceability**: Added debug logs in `decorator.py` and `registry.py` to track:
    - Start and end of digestion per function.
    - Pipeline execution per argument.
    - Warnings for missing rules.

### 4. Native Integrations (First-Class Citizens)
- **Native Beartype Support**: Added `type_check=True` parameter to `@digest`. If enabled, it automatically applies `beartype` to the function, ensuring type hints are enforced on the *digested* values.
- **Native Pydantic Support**: The `Registry` now recognizes Pydantic models passed directly as rules. If a rule is a Pydantic class, it automatically calls `model_validate()`, providing seamless structural validation.

### 5. Dependency Management
- Updated `pyproject.toml` with `optional-dependencies` for `beartype` and `pydantic`.
- Updated `devtools/conda-envs/development_env.yaml` to include them in the dev environment.

### 6. Test Suite Consolidation
- Integrated all new feature tests into `tests/test_decorator.py` and `tests/test_argument_digestion.py`.
- Added `tests/test_logging.py`, `tests/test_errors.py`, `tests/test_beartype.py`, and `tests/test_pydantic.py`.

---
## Next Steps
- [ ] **Phase 3: Documentation**: Generate API reference using Sphinx.
- [ ] **CI/CD**: Setup GitHub Actions for automated testing.
- [ ] **Built-in Pipelines**: Implement `argdigest.pipelines.base_coercers` and `base_validators`.
