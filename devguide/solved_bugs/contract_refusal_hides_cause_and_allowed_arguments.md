---
summary: A function-contract refusal hid a reserved-token error and the arguments accepted for the call.
issue: uibcdf/argdigest#14
status: resolved
opened: 2026-09-22
closed: 2026-09-26
severity: medium
verification: reproduced
area: [api, diagnostics]
guard: tests/test_function_contract.py::test_dynamic_domain_rejection_shows_current_accepted_names
normative:
blocked_by: []
supersedes: []
---

# Contract refusal hides its cause and accepted arguments

## What

`FunctionContract(admits=["signature", "format_options"])` treated the reserved
`signature` token as a domain name. A valid call could then fail with an
unregistered-domain error. An actually unknown keyword was rejected without
showing the admissible names that would help the caller correct it.

## How

The reserved `signature` and `any` tokens are excluded from domain names in a
sequence. `any` retains its permissive meaning there. On an unknown keyword,
the contract now adds the resolved names for that call to its hint, including
the current branch of a value-dependent domain. It caps the displayed list at
ten names and states how many more exist. A direct regression checks the
sequence token and the dynamic hint; an end-to-end regression checks the
rendered `UnknownArgumentError` from a consumer-style function.

## Why

The first failure blames a caller for a declaration token that ArgDigest
misread. The second leaves the caller without the short set of names already
known to the contract, especially for value-dependent `**kwargs`.

## Acceptance criteria

- Reserved admission tokens in a sequence are not treated as domain names.
- A rejected keyword shows the names admissible for that call, without names
  from other branches of a value-dependent domain.
- The public error text includes the hint; large domains stay readable.

## Resolution

`tests/test_function_contract.py::test_dynamic_domain_rejection_shows_current_accepted_names`
guards the public error text. The direct sequence-token and dynamic-domain
tests guard the exact `FunctionContract` behavior.
