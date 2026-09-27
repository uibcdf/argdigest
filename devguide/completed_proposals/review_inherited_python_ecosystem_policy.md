---
summary: Review inherited Python ecosystem policy in ArgDigest.
issue: uibcdf/argdigest#20
status: resolved
opened: 2026-09-24
closed: 2026-09-27
verification: measured
area: [governance, dependencies, ci]
guard: tests/test_pyunitwizard.py::test_puw_integration_check_and_standardize
normative:
blocked_by: []
supersedes: []
---

# Review inherited Python ecosystem policy in ArgDigest

## What

ArgDigest follows MolSysSuite's Python developer-tools and support-library policies.
A synchronized guide and compatible policy caller do not
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
- PyUnitWizard is an optional physical-quantity adapter. Pin published 0.27.0
  in both test environments, including the core environment used on Windows
  and Python 3.14. Import it explicitly before tests so an accidental skip
  cannot pass CI, and exercise its `check`, `standardize`, `convert`, and
  quantity-extraction paths across every claimed Python minor.

## Why

The developer-tool changes satisfy the inherited CI presentation and release
pin requirements. The published optional integration now has hosted evidence
across the complete claimed Python and operating-system matrix.

## Evidence and current state

Source commit `1d8e337726ee9647aa3a56671b5c6c7def063257` contains the
developer-tool changes. The isolated local checkout passed 274 tests with
`python -m pytest --receptor=llm -q tests`, full-tree Ruff check and format,
the developer-guide index check, and MolSysSuite's repository checker.

The exact-commit routine CI `36064688726` passed with 273 tests and one
skip; its log confirmed published `pytest-receptor 1.1.0 py_1` from
`uibcdf` and `--receptor=ci`. The shared policy run `36064689045` passed.
The full Python/OS matrix `36101321876` passed 12/12 cells, and the
Python 3.14 feasibility run `36101321962` passed 3/3. GH Run Receptor
inspected all four runs. The developer-tools review is therefore adopted.

Source commit `d6dcebef9174ad2427aeea8711394afeea880bcf` installed
PyUnitWizard 0.27.0 from the public Conda channel in both CI environments and
made routine CI and the full matrix fail if the adapter cannot be imported.
Local `tests/test_pyunitwizard.py` passed all seven integration tests; the full
suite passed 283 with one unrelated sibling-checkout skip. Exact-commit routine
CI `36335205697`, policy `36335206079`, and full matrix `36335240891` all
passed. GH Run Receptor inspected each run. The matrix completed 12/12 jobs
on Linux, macOS, and Windows with Python 3.11–3.14. Each native job log showed
PyUnitWizard 0.27.0 imported and 283 tests passed with the same one unrelated
skip. These runs establish the optional published integration without adding
PyUnitWizard to ArgDigest's required runtime dependencies.

The selected guard exercises a physical dimensionality rule using the optional
adapter. Its skip remains valid for a lean local checkout; the CI import step
and pinned environments make that guard active in the hosted matrix.

## Acceptance criteria

- Local tests pass with pytest-receptor's `llm` profile; Ruff, reporting index,
  and MolSysSuite conformance checks pass.
- Hosted routine CI, policy, full matrix, and Python 3.14 probe confirm the
  exact release pin and `ci` profile on the same source commit.
- MolSysSuite records developer-tools and support-libraries adoption with
  separate evidence from their exact implementation commits.
