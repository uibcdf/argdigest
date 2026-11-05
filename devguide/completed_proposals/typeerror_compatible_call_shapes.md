---
summary: Retain Python TypeError catches for unknown and missing argument refusals.
issue: uibcdf/argdigest#48
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: reproduced
area: [contracts, compatibility]
guard: tests/test_call_shape_errors.py
normative:
blocked_by: []
supersedes: []
---

# TypeError-compatible call-shape refusals

## What

Adopting ArgDigest changed unsupported-keyword refusals from native TypeError to
an exception outside that catch family. The request concerns compatibility, not
admitting invalid calls. Consumer ownership is uibcdf/pharmacophoremt#82 / #6.

## How

Use compatible inheritance: `UnknownArgumentError` and `MissingArgumentError`
retain their class identities and FunctionContractError/DigestError ancestry
while also inheriting TypeError. Their catalog codes/context and rebuild behavior
are unchanged. No opt-in knob or consumer catch/validation shim is necessary.
Unknown arguments are refused before the callable body; normal and explicit
False calls keep typed catalog refusals, and literal True keeps native bypass.
Missing groups represent invalid call shape too. ArgumentConsistencyError and
unknown-domain declaration errors retain their previous families; value/schema
errors are not reclassified. The guards exercise both decorator forms, bypass
contrasts and args/deepcopy/pickle reconstruction. Existing domain/required-group
assertions remain in the complete source suite.

## Why

This extends catch compatibility without changing error identities or weakening
admission. Public 0.17.0 retains its old hierarchy; consumer receiving must use
a future published correction before relying on TypeError compatibility.
