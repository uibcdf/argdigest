# Strictness and Errors

ArgDigest has **two** policies, for two different mistakes:

| Policy | Fires when | Whose mistake | Default |
| --- | --- | --- | --- |
| `strictness` | a declared parameter has no digester | the library author | `warn` |
| `unknown_argument` | a keyword is outside the function's contract | whoever made the call | `error` |

They are deliberately separate. A missing digester is a to-do for you and can wait behind
a warning. A keyword nobody declared is a caller's typo, and a warning is not enough for
it: warnings are routinely filtered off exactly where users read output, and the call
would then run with the default and hand back a plausible wrong answer.

## Strictness modes

`strictness` controls how hard your contract is when digestion coverage is not
complete. During migration, `warn` is usually the safest start because it keeps
runtime behavior visible without immediately breaking calls. Once coverage is
stable, `error` is a better default because it enforces the contract and catches
integration regressions early. `ignore` exists for exceptional scenarios, but it
should be used carefully because it can hide real coverage gaps.

Accepted aliases:
- `error` or `raise`
- `warn` or `warning`
- `ignore`, `silent`, or `none`

Example:

```python
@arg_digest(strictness="error")
def get(...):
    ...
```

## The `unknown_argument` policy

```python
@arg_digest(unknown_argument="warn")   # error | warn | ignore
def get(...):
    ...
```

`error` is the default because **ArgDigest must never end up more permissive than the
language it wraps**: plain Python already raises `TypeError` for an unexpected keyword,
and a decorated function must not start accepting one. Use `warn` while cleaning up an
existing codebase, and `ignore` only to reproduce the pre-`0.10.0` behaviour.

## Core exception model

Main error types:
- `DigestError` (base class),
- `DigestTypeError`,
- `DigestValueError`,
- `DigestInvariantError`,
- `DigestNotDigestedError`.

Function contract errors, all deriving from `FunctionContractError`:
- `UnknownArgumentError` — an argument the function does not accept, with a near-miss
  suggestion when one is close;
- `MissingArgumentError` — a call satisfying no required argument group;
- `ArgumentConsistencyError` — mutually exclusive or co-required arguments misused.

Warnings:
- `DigestNotDigestedWarning`,
- `FunctionContractWarning` — the contract errors above, when `unknown_argument="warn"`.

## Error context

ArgDigest errors include contextual data such as:
- function name,
- argument name,
- offending value,
- optional hint for resolution.

This context is important for both user diagnostics and maintenance workflows.
It allows support teams to understand failures quickly and helps contributors
reproduce issues without digging through unrelated code paths.

## Dependency cycles between digesters

If digester dependencies are cyclic (for example, `a` depends on `b` and `b`
depends on `a`), ArgDigest raises a digestion error describing the cycle path.

## Migration guidance

A practical migration flow is: start with `strictness="warn"` while coverage is
incomplete, track warnings in tests/CI, and then move to
`strictness="error"` when digestion coverage becomes stable and intentional.

## Next

Continue with [Migration: warn to error](migration-warn-to-error.md).
