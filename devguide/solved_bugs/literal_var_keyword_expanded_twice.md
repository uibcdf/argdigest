---
summary: Preserve literal VAR_KEYWORD-named options without changing named arguments.
issue: uibcdf/argdigest#47
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: reproduced
severity: high
area: [arguments, binding]
guard: tests/test_literal_var_keyword.py
normative:
blocked_by: []
supersedes: []
---

# Literal VAR_KEYWORD expanded twice

## What

PharmacophoreMT reported that `delegate('original', kwargs={'file_name': 'changed'})`
can replace its explicit source. The callable body receives the wrong routing
input; no incorrect molecular calculation is claimed by the consumer spy.

## How

`core.utils.bind_arguments` already flattens the VAR_KEYWORD container. Removed
only the wrapper's second expansion/removal. Literal opaque, None, empty and
mapping options retain identity and undergo ordinary alias/domain admission.
The reusable binder documents its single-flattening output contract.
Sixteen initial failures across the #47/#48 guards were observed before the
repairs; the relevant #47 failures include argument replacement, lost options,
variadic call shape and missing domain refusal. Native/bypass contrast controls
already passed. Alternate kwargs/options names, closed domain refusal and
aliases now pass with the other source tests.

## Why

Generic argument binding belongs in ArgDigest, not a downstream renaming or
validation engine. The regression exercises the exact routing corruption mechanism.
Source is repaired; public 0.17.0 is unchanged. PharmacophoreMT #82 remains
blocked until a subsequently published correction is received.
