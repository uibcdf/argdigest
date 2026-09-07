# AGENTS

## External Tooling Guides (Required for Development)

These guides are required reading for anyone developing this library. They describe how external tools must be used here.

- `SMONITOR_GUIDE.md` — Required guide for SMonitor integration and diagnostics.
- `GH_RUN_RECEPTOR_GUIDE.md` — Required guide for compact, truth-preserving inspection of
  GitHub Actions runs and the native-command fallback.
- `MOLSYSSUITE_GUIDE.md` — Required suite-governance guide; this synchronized copy must
  not be edited locally.

## MolSysSuite coordination

- ArgDigest is a member of MolSysSuite.
- Report and document suite-wide policies, cross-repository proposals, and shared tooling
  problems in `uibcdf/molsyssuite`.
- Keep ArgDigest-specific implementation, tests, releases, and product issues in this
  repository.
- Follow `devguide/reporting_protocol.md` for the issue-backed lifecycle of local bugs
  and proposals; it maps the common `uibcdf/molsyssuite#11` contract to local paths.
- Follow the versioned policy caller in `.github/workflows/molsyssuite-policy.yml`; do not
  duplicate its common checks in repository-owned workflows.
