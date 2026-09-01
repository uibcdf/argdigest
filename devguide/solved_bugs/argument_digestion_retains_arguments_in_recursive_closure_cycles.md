---
summary: Argument digestion retains arguments in recursive closure cycles.
issue: uibcdf/argdigest#3
status: resolved
opened: 2026-09-01
closed: 2026-09-01
severity: high
verification: reproduced
area: [digestion, performance]
guard: tests/test_argument_digestion.py::test_argument_digestion_does_not_retain_arguments_in_a_reference_cycle
normative:
blocked_by: []
supersedes: []
---

# Bug: argument digestion retains arguments in recursive closure cycles

## What

Every ordinary `@arg_digest` call creates a local recursive `gut` function. The function
closes over itself as well as the call's bound arguments, so those arguments remain alive
until Python's cyclic garbage collector runs.

The retained objects are small in an isolated ArgDigest call. The consequence becomes
material in consumers that compensate by calling `gc.collect()` at every public return,
or in processes that deliberately disable automatic cyclic collection.

## How

A weak-reference probe reproduces the retention without relying on object counts or
implementation-specific garbage layouts:

1. Decorate a function accepting a weak-referenceable payload.
2. Disable automatic cyclic garbage collection.
3. Call the function and delete the caller's payload reference.
4. Observe that the weak reference remains alive until `gc.collect()` runs.

In MolSysMT, 1,000 `get_center` calls with its explicit collections suppressed retained
72,000 cyclic objects while automatic GC was disabled. Inspection found recursive
`argdigest.core.decorator...gut` closures, cells, dictionaries, lists, and tuples; no
NumPy arrays were members of those cycles. The downstream performance defect is tracked
as `uibcdf/molsysmt#183`.

## Why

Arguments should become collectible when an ordinary decorated call returns. Requiring
consumer libraries to trigger global full-generation collection couples a local
validation detail to the size of the entire Python process heap. MolSysMT measured that
work at 40 to 58 times the computation performed by several public structure functions.

## Intended outcome

Keep recursive dependency resolution and cycle diagnostics unchanged, but remove the
self-reference from the per-call traversal closure. A completed call must not retain an
otherwise unreachable argument when automatic cyclic GC is disabled.

## Acceptance criteria

1. The weak-reference probe passes without an explicit collection between the call and
   the assertion.
2. Recursive argument dependencies are still resolved in dependency order.
3. Cyclic dependencies still raise `DigestNotDigestedError` with the complete path.
4. The ArgDigest test suite and Ruff checks pass, apart from independently documented
   environment or baseline failures.

## Risks

Changing recursion mechanics could break dependency ordering or cycle reporting. The
existing dependency and cyclic-dependency tests are therefore part of the required
guard set.

## Resolution

Resolved in `fd09a24`. Recursive visits now receive their traversal callable explicitly,
so the local function no longer closes over itself. This preserves dependency ordering
and cycle diagnostics while allowing bound arguments to be released by reference
counting when the decorated call returns.

The complete suite passes with 222 tests under Python 3.13. The integrated MolSysMT
probe leaves no unreachable ArgDigest objects after 1,000 calls with automatic cyclic
GC disabled, and its RSS delta falls from about 99 MiB to about 0.01 MiB in that probe.
