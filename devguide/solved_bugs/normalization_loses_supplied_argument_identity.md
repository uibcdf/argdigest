---
summary: Preserve canonical supplied names through normalization and function contracts.
issue: uibcdf/argdigest#38
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: high
verification: reproduced
area: [contracts, normalization, binding]
guard: tests/test_contract_owner.py
normative:
blocked_by: []
supersedes: []
---

# Normalization loses supplied argument identity

## Completion — 2026-10-22

The complete Python 3.14.7 source suite passes 456 tests without omissions.
The guard now exercises each ownership mode across alias presence rules,
closed signatures, canonical-name collisions, unknown names and variadic
calls. Separate normalization-unit tests prove that canonical supplied-name
output leaves the original input set unchanged, including no-match paths.
The new regression tests failed before the correction, so the guard checks
the reported mechanism rather than only the returned values of digesters.

## What

Final review of #37 at `ca172d68a78190836031d0602580bd6a2203a9d2` found
that a canonical value supplied through an alias could be treated as a default
by function-contract presence rules. The defect also affects the original
runtime-owner mode. It can refuse valid calls and admit forbidden combinations.

## How

Declare `short -> value` where `value` has a default. A call using `short=7`
normalizes its bound mapping to `value=7`, but the wrapper reconstructs the
supplied set from raw kwargs and positional counts, losing the canonical name.
Nine reproduced failures cover required, co-required and mutually exclusive
rules across default, definition and exact ownership. Further checks reproduce
three closed-signature alias refusals and three cases where `*args` incorrectly
make an omitted keyword-only default appear explicitly supplied.

The correction carries binding's original supplied set forward instead of
reconstructing it. `core/normalization.py::apply_normalization` optionally
reports canonical names into a fresh `supplied_out`, retaining the legacy
mapping return and leaving its input set untouched. The wrapper translates
held-aside closed-signature extras before admission and retains genuine unknown
names for the existing refusal path. Arbitrary standardizers retain their
existing mapping contract; no type/value or callable-body inference is added.

## Why

Alias spelling must not change argument-contract semantics. The normalization
owner already knows the exact renames; the consumer should use its result
rather than attempting to infer provenance again from call shape.

## Acceptance criteria

- Aliases and canonical names agree for all three presence-rule families.
- Declared aliases work for closed signatures; collisions and typos still fail.
- Defaults remain absent unless supplied, even with variadic positional calls.
- Both ownership opt-ins and the default path remain covered.
- Reusable normalization output preserves its input presence set.
