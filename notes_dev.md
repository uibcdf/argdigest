# Development Notes - ArgDigest

## 2026-01-31: Phase 4 (v0.4.0) Implementation ✅
- **Declarative Config**: Support for YAML/JSON files.
- **Data Science**: Numpy and Pandas specialized pipelines.
- **Performance**: Execution profiling and audit logs.
- **Quality**: Reached 90% coverage and configured Codecov.

## Phase 5: Performance & CLI Tooling (0.5.0) ✅
- **Digestion Plan Caching**: Implemented `DigestionPlan` to pre-calculate logic at decoration time, reducing runtime overhead to near-zero.
- **CLI Audit Tool**: Added `argdigest audit` to inspect rules applied to functions.
- **AI Agent Support**: Added `argdigest agent init/update` to generate and maintain `ARG_DIGEST_AGENTS.md` instructions for AI assistance.
- **Quality**: Maintained high coverage and added `.coveragerc`.

### 3. Release Automation (CI/CD Final) ✅
- **Auto-Release**: Configured GitHub Actions to automatically create GitHub Releases and publish to Conda on tag push.
- **Shared Action**: Updated `uibcdf/action-build-and-upload-conda-packages` to v1.5.0 with native release support.

### 4. Code Quality & Cleanup ✅
- **Linting**: Enforced `ruff` standards, removing unused imports and cleaning up the codebase.
- **Coverage**: Maintained >90% test coverage across the entire project.

## Phase 6: Pilot Integration (0.6.0) 🚀
- **Target**: MolSysMT.
- **Objective**: Replace the legacy digestion engine with ArgDigest in key modules.
- **Validation**: Ensure all scientific workflows and unit systems remain consistent.

---
## Next Steps
- [ ] Begin migration of `molsysmt.basic.get`.
- [ ] Verify PyUnitWizard context management in real MolSysMT scenarios.