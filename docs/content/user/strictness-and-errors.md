# Strictness and Errors

ArgDigest can warn, fail, or ignore when an argument has no digester.

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

## Core exception model

Main error types:
- `DigestError` (base class),
- `DigestTypeError`,
- `DigestValueError`,
- `DigestInvariantError`,
- `DigestNotDigestedError`.

Warnings:
- `DigestNotDigestedWarning`.

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
