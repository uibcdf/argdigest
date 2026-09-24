---
summary: Review inherited Python ecosystem policy in ArgDigest.
issue: uibcdf/argdigest#20
status: active
opened: 2026-09-24
closed:
verification: inspected
area: [governance, dependencies, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review inherited Python ecosystem policy in ArgDigest

## What

ArgDigest inherits MOLI's Python developer-tools and support-library policies
through MolSysSuite. A synchronized guide and compatible policy caller do not
establish their adoption. The routine, full-matrix, and Python 3.14 feasibility
workflows used pytest-receptor's `llm` profile in hosted logs, and the two
test environments did not pin an exact published receptor release.

## How

Use the published pytest-receptor 1.1.0 release in both CI test environments.
Select its `ci` profile for all three hosted pytest commands without changing
test selection, coverage, or exit status. Configure rerun commands for the
repository's `python -m pytest` invocation. Keep the `llm` profile for local
agent-driven tests. Inspect exact-commit hosted runs first with GH Run Receptor.

Review the inherited support-library boundaries separately:

- ArgDigest itself provides public argument validation and does not depend on
  another copy of ArgDigest.
- DepDigest is a runtime dependency for optional integrations, and SMonitor is
  a runtime dependency for diagnostics. Both have exercised implementation
  paths and dedicated tests.
- PyUnitWizard is an optional physical-quantity adapter. Its `check`,
  `standardize`, `convert`, and quantity-extraction paths have tests, but the
  optional integration still needs exact published-release evidence on every
  Python minor ArgDigest claims, including Python 3.14. Keep this review
  partial until that evidence or a bounded exception is recorded.

## Why

The developer-tool changes satisfy the inherited CI presentation and release
pin requirements. An honest partial support-library review prevents optional
integration code from being mistaken for verified public support.

## Acceptance criteria

- Local tests pass with pytest-receptor's `llm` profile; Ruff, reporting index,
  and MolSysSuite conformance checks pass.
- Hosted routine CI, policy, full matrix, and Python 3.14 probe confirm the
  exact release pin and `ci` profile on the same source commit.
- MolSysSuite records developer-tools and support-libraries states with
  separate evidence, retaining any unresolved optional-integration check in
  `uibcdf/argdigest#20`.
