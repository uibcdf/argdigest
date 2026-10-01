# AGENTS

## External Tooling Guides (Required for Development)

These guides are required reading for anyone developing this library. They describe how external tools must be used here.

- `SMONITOR_GUIDE.md` — Required guide for SMonitor integration and diagnostics.
- `GH_RUN_RECEPTOR_GUIDE.md` — Required guide for compact, truth-preserving inspection of
  GitHub Actions runs and the native-command fallback.
- `PYTEST_RECEPTOR_GUIDE.md` — Required guide for compact, truth-preserving pytest output
  in local and hosted development.
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

## Modular reusable tools

Before adding a feature, inspect existing tools and identify the owning module or
component. Implement or extend independently useful operations as documented reusable
tools in that owner, with their own contracts and tests; have consumers call them.
Keep task-specific decisions local and report missing sibling capabilities to the
provider with linked consumer evidence. Follow
[MOLSYSSUITE_GUIDE.md#modular-reusable-tools](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
for applicability, compatibility, performance and tracked exceptions.
