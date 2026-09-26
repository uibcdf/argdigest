---
summary: A decorated classmethod treated its implicit cls receiver as an undigested argument.
issue: uibcdf/argdigest#19
status: resolved
opened: 2026-09-24
closed: 2026-09-26
severity: medium
verification: reproduced
area: [api, validation]
guard: tests/test_argument_digestion.py::test_classmethod_receiver_is_not_digested_in_either_decorator_order
normative:
blocked_by: []
supersedes: []
---

# Classmethod receiver is digested

## What

ArgDigest skipped `self` during pipeline target construction and argument
digestion, but processed `cls` as a caller-supplied argument. A classmethod
therefore emitted a missing-digester warning, or failed with strictness
`error`, even when every actual caller argument had a digester.

## How

The regression uses strictness `error` and checks both classmethod decorator
orders. Before the fix, ArgDigest could not inspect a `classmethod` descriptor
when it was the inner decorator. The decorator now unwraps and rewraps that
descriptor. It excludes the first `cls` parameter of a method from automatic
pipeline and argument digestion. A separate test asserts that a free function
with a parameter named `cls` still digests it.

## Why

Python supplies the classmethod receiver. Treating it as an undigested user
argument prevents consumers from applying strict validation to classmethods.

## Acceptance criteria

- Both classmethod decorator orders accept and digest real caller arguments.
- The implicit class receiver requires no digester or pipeline rule.
- A free function parameter named `cls` remains an ordinary argument.

## Resolution

`tests/test_argument_digestion.py::test_classmethod_receiver_is_not_digested_in_either_decorator_order`
guards the failure mechanism in both decorator orders. The companion free
function test guards the scope of the receiver exception.
