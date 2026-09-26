---
summary: A truthy non-boolean skip_digestion bypasses validation before its digester runs.
issue: uibcdf/argdigest#17
status: resolved
opened: 2026-09-24
closed: 2026-09-26
severity: high
verification: reproduced
area: [api, validation]
guard: tests/test_argument_digestion.py::test_only_literal_true_skips_digestion_before_validating_the_flag
normative:
blocked_by: []
supersedes: []
---

# Truthy non-boolean skip_digestion bypasses validation

## What

The decorator checked the truthiness of the configured skip argument before
running any digester. `skip_digestion="yes"`, `1`, or even the string `"False"`
therefore bypassed both argument digestion and the function contract. A
consumer's `digest_skip_digestion` could not reject those values.

## How

`tests/test_argument_digestion.py::test_only_literal_true_skips_digestion_before_validating_the_flag`
reproduced the defect: before the fix, a keyword call with `"yes"` returned
without raising the expected validation error. The same early return existed
after positional argument binding. Check `is True` at both bypass sites so all
other values follow normal digestion. Keep the literal-`True` fast path and
ordinary `False` path intact. Document the precise contract in the user guide
and canonical ArgDigest integration guide.

## Why

ArgDigest is the argument-validation boundary for consumers. A string or
integer unintentionally disabling all checks violates the purpose of that
boundary. `uibcdf/sabueso#31` supplied a concrete public-API reproduction;
this is provider behavior and belongs in ArgDigest.

## Acceptance criteria

- Literal `True`, passed by name or position, still bypasses digestion.
- Non-boolean truthy values reach the skip-flag digester and are rejected when
  that consumer requires a boolean.
- `False` still takes the normal digestion path.
- The canonical guide states the literal-boolean rule; registered consumers
  receive their copy through MolSysSuite's guide synchronizer.

## Resolution

Both bypass checks now require literal `True`. The regression asserts that
keyword and positional `True` bypass digestion, `False` takes the normal path,
and strings and integers reach the skip-flag digester for rejection. The
canonical guide was distributed with MolSysSuite's guide synchronizer to all
seven registered consumers. The ArgDigest CI and MolSysSuite policy runs for
`acbead8` passed; the local test suite passed with 274 tests and 1 skip.
