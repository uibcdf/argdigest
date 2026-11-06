---
summary: Keep diagnostic label lookup off valid digester metadata paths.
issue: uibcdf/argdigest#53
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [diagnostics, digestion, compatibility]
guard: tests/test_consumer_digester_diagnostics.py
normative:
blocked_by: []
supersedes: []
---

# Eager digester identity lookup

## What

Final pre-build review of #50 found an unpublished-candidate regression at
cb97df7: a valid callable with an unambiguous signature could fail because its
metaclass rejects diagnostic label attributes. Exact previous 5b61925 accepts
it; cb97df7 reads __module__/__qualname__ before value-parameter resolution and
raises the unrelated label error. No 0.17.1 package had been built or uploaded.

## How

Resolve exact-name/sole-value signatures first. Only an actual ambiguity may
look up a label, and only under detailed capture. Missing, opaque or failing
label metadata keeps a fixed identity and the intended DigestNotDigestedError;
it cannot replace validation or trigger payload conversion. Successful metadata
alone is cached. The #50 classification, context and corrective hint remain.

The expanded fourteen-control module fails six controls on cb97df7 (eight pass):
two valid callable registrations, two failing-label ambiguity cases, and two
opaque-label/capture cases. Both exact-name and sole-value valid callables now
execute without label reads. The corrected complete local source selection
passes 534 tests including collective E2E and nested receiving, without skips;
three known missing-digester warnings remain. These source checks inherit
editable siblings and do not replace #51's exact-file qualification.

Two existing #46 emission-fallback mocks also resolve/stub DepDigest availability
before installing their artificial import failures, so they work independently
of earlier test-module imports. Their intended missing-checker/emission failure
assertions remain unchanged; both isolated controls pass.

## Why

Diagnostic-only metadata must not reject a valid consumer or replace the owning
configuration error. The guard asserts whole registered-consumer execution,
zero unnecessary reads/conversions and the unchanged error/code/context on
actual ambiguity. The superseded candidate's source runs are not release gates;
the corrected SHA must receive all of #51's required source/installed matrices.

## Public delivery — 2026-11-05

0.17.1 is published with this correction. Independent original-file source,
full installed, minimal-core and fresh public receiving evidence is archived
under release #51 in `devguide/completed_proposals/release_0_17_1.md`.
The earlier source-only measurements above retain their original scope.
