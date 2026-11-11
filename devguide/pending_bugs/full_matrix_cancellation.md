---
summary: Let the full source matrix honor ordinary workflow cancellation.
issue: uibcdf/argdigest#52
status: active
opened: 2026-11-05
closed:
severity: medium
verification: measured
area: [ci, cancellation]
guard: tests/test_full_matrix_cancellation.py
normative:
blocked_by: []
supersedes: []
---

# Full source matrix cancellation

## What

During 0.17.1 qualification, an ordinary cancellation was acknowledged but the
source matrix remained queued and required force-cancel. The job uses `always()`.
GitHub documents reevaluation of job conditions during cancellation and recommends
`!cancelled()` for work that should survive failures but stop on cancellation.
This explains a cancellation hazard; it does not establish a macOS queue cause.

## How

Replace only the full-test status guard with `!cancelled()`. Preserve the
administrative probe, nightly debt decision and failure recovery, weekly/manual
execution, all twelve platform/interpreter cells, tests and environment routes.
Refresh the reviewed workflow digest in the existing dependency inventory.

The regression guard checks the explicit negative cancellation status and the
existing dependency/concurrency boundary. Check the retained selection against
explicit event/input/needs scenarios using the existing shared condition tool;
those controlled status fixtures are not native execution evidence. Verify a
normal cancellation on one owned, exact-source hosted matrix separately, without
force-cancel or a claim that cancelled scientific jobs passed.

## Why

An expensive scientific matrix must yield to an operator cancellation without
changing recovery coverage. This affects development orchestration; the immutable
0.17.1 tag/file and its completed qualification remain unchanged.

## Acceptance criteria

- The regression guard fails on the previous `always()` condition.
- Noncancelled nightly/manual/weekly selections and probe exclusion are retained.
- All twelve configured scientific cells and dependency-route checks remain.
- One owned hosted matrix completes ordinary cancellation without force-cancel.
- Applicable final-head CI passes and the report/issue lifecycle is synchronized.

## Local checks — 2026-11-10

The new workflow guard fails on the old condition (one expected failure).
After replacing the status guard, 58 selected cancellation/backlog, matrix,
workflow-YAML, reporting and publication-route checks pass. The existing debt
regression now explicitly includes cancelled and unfinished runs. Ruff lint
and formatting and the pinned dependency preflight pass; all twelve cells remain.

Eighteen configured scenarios reuse MolSysSuite's existing `condition_outcome`
operation with an explicit cancelled-status fixture. Noncancelled selection is
unchanged and all cancelled scenarios refuse execution. This is bounded
configuration analysis, not a native runner or scientific qualification.

Local source checks use published Pytest Receptor 1.2.2 on Python 3.14. They
do not establish scientific/public-artifact qualification. Native cancellation
and hosted final-head CI remain separate required checkpoints for this fix.
