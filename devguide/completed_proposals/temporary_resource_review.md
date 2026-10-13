---
summary: Preserve caller resources and complete ArgDigest's bounded tool closeout.
issue: uibcdf/argdigest#33
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: medium
verification: reproduced
area: [testing, tools, resources]
guard: tests/test_cli_resource_ownership.py::test_real_cli_tests_preserve_caller_files_and_retire_outputs
normative: devguide/resource_lifecycle_review.md
blocked_by: []
supersedes: []
---

# Temporary-resource disposition

## What

Complete the incoming owner review from uibcdf/molsyssuite#104. The two real
agent CLI tests overwrote a synthetic caller document; init additionally deleted
it, and update left output behind. All three original nodes passed, so ordinary
green test status did not establish caller custody.

## How

A function-scoped TemporaryDirectory fixture changes cwd under a nested
monkeypatch context, restores cwd before cleanup and propagates cleanup errors.
Four subprocess guards run the actual nodes on success and controlled failure
after writing, with a caller-owned sentinel and private scratch. They assert
exact sentinel bytes and no remaining child scratch before parent retirement.
The production CLI still writes its caller-requested output normally.

The maintained operation contract reviews runtime, files, config, threads,
processes, namespaces, devtools, docs/build/qualification and hosted callers.
Eight obsolete 0.14.0 roots were explicitly audited and retired. Small immutable
receipts are retained under a purpose and review date; shared/user/foreign
resources were preserved. Details are in resource_lifecycle_review.md.

The dated, bounded disposition receipt is
`devguide/evidence/resource_review_33_2026_10_13.json`. It records observed
pre-removal ownership checks separately from current-task removal verification;
it does not infer who removed unrelated historical paths.

## Why

Tests must not delete a human document merely because a generated filename
matches. A closed release does not justify keeping disposable prefixes or
snapshots indefinitely; neither does absence prove historical disposal or a
global inventory. This bounded owner disposition separates executed custody
from source inspection and external-provider/scientific evidence.

## Acceptance criteria

- Real CLI tests preserve caller documents after success and failure.
- Current task and old owned disposable roots have explicit retirement receipts.
- Retained useful evidence and borrowed resources have clear custody/lifetime.
- Guard, maintained contract, issue state/archive and MolSysSuite #104 handoff agree.
