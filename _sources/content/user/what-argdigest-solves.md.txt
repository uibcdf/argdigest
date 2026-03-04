# What ArgDigest Solves

ArgDigest is designed for libraries that need consistent argument handling at
API boundaries.

## What ArgDigest does

ArgDigest gives you a dedicated layer where argument behavior is defined once and
reused everywhere. In practice, this means you can normalize names before
validation, digest values with explicit per-argument functions, and compose
reusable validation/coercion rules with pipelines. It also gives you explicit
policy control for missing digesters (`warn`, `error`, `ignore`) and structured
errors with contextual information for debugging and support.

## What ArgDigest does not do

ArgDigest does not replace your domain model or make scientific decisions for
your library. It does not force a single package layout either, and it is not a
substitute for thoughtful API design and testing. Its role is narrower and more
practical: make argument handling coherent and maintainable.

## Typical value in scientific libraries

Scientific libraries often accumulate repeated input checks, alias handling, and
type coercions in many modules. ArgDigest centralizes that behavior so business
functions stay focused on domain logic. As a result, argument behavior becomes
more predictable across entry points, and invalid inputs fail with clearer and
more consistent messages.

## Before vs After (practical)

Before ArgDigest, validation logic is usually repeated across API functions,
argument aliases are handled inconsistently, and failure messages vary from one
module to another. After ArgDigest, digestion contracts live in one place,
aliases are normalized systematically, and errors follow a consistent structure
with contextual hints.

## Advantages for maintainers

Maintainers get a simpler contribution surface because argument behavior is
located in one layer. Refactors are safer because rules are reusable and easy to
test in isolation, and teams can harden behavior gradually by moving from
`warn` to `error` when coverage is mature.

## When to adopt first

Start with modules where:
- argument semantics are repeated,
- user errors are frequent,
- normalization logic is currently scattered.

## Next

Continue with [Quick Start](quickstart.md).
