---
summary: Method caller names the module and method but omits the runtime class.
issue: uibcdf/argdigest#18
status: resolved
opened: 2026-09-24
closed: 2026-09-26
severity: medium
verification: reproduced
area: [contracts, diagnostics]
guard: tests/test_qualified_caller.py::test_method_digester_receives_runtime_qualname_without_changing_caller
normative: standards/ARGDIGEST_GUIDE.md
blocked_by: []
supersedes: []
---

# Method caller omits the runtime class

## What

The `caller` given to a method's digester is `<owner module>.<method>`. Sabueso saw
messages such as `sabueso.core.card.extract` without `Card`, even though it was the
class that made the refusal understandable.

## How

ArgDigest now injects an optional `qualname` parameter when a digester declares it.
For a method, that value uses the runtime receiver's module and class name. For free
functions it uses the qualified function name. The existing `caller` stays unchanged
for contract lookup, normalization, standardizers, and existing digesters. A digester
can use `qualname` in its own user-facing refusal message.

## Why

Changing `caller` directly would silently change function-contract keys used by
consumers such as MolSysMT. The second name gives new digesters enough context for
diagnostics without altering those keys.

## Evidence

The regression checks inherited instance and class methods, plus a runtime class in a
different module. It asserts the old caller key and the new runtime class-qualified
name. A second test uses `qualname` in a refusal. Both passed on Python 3.13 on
2026-09-26.

## What was refuted

- Replacing the caller string was rejected because it is also a contract key.
- Using only the defining class would misname inherited and mixin-assembled methods.

## Scope and exclusions

Existing digesters keep their signatures and messages until they opt into `qualname`.
ArgDigest does not rewrite arbitrary exceptions raised by consumer digesters.

## Acceptance criteria

- Method digesters can receive the runtime class-qualified name.
- The contract and standardizer caller key remains byte-identical.
- Existing digesters without `qualname` continue to work.
