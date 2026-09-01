# Implementation Patterns

These patterns help evolve ArgDigest without breaking downstream integrations.

## Pattern 1: contract-first evolution

- Define expected behavior before implementation changes.
- Keep documentation and tests aligned with contract decisions.

## Pattern 2: explicit precedence

When adding new configuration behaviors, keep precedence stable:
1. decorator arguments,
2. explicit config module,
3. environment config module (`ARGDIGEST_CONFIG`),
4. auto-discovery defaults.

## Pattern 3: migration-safe defaults

- Prefer non-breaking defaults in minor versions.
- Introduce stricter behavior behind explicit options first.

**With one standing exception, taken in `0.10.0`:** ArgDigest must never end up more
permissive than the language it wraps. Plain Python raises `TypeError` for an unexpected
keyword and a decorated function accepted it, so `unknown_argument` defaults to `error`
even though that breaks calls that used to pass. Shipping a stable release on top of that
would have frozen the anomaly into the contract every downstream library depends on.

A default that makes ArgDigest weaker than plain Python is a defect, not a
migration-friendly choice, and it should be corrected rather than deferred.

## Pattern 4: architecture freedom for adopters

Do not force one digestion layout. Preserve support for:
- package style,
- registry style,
- decorator style,
- mixed mode.

## Pattern 5: rules are data, dispatch is lookup

All three declaration mechanisms — argument digesters, function contracts and alias
tables — follow the same shape, and new ones should too:

- the consumer declares **data**, discovered by scanning a package it names in its config;
- ArgDigest owns discovery, resolution order, enforcement and diagnostics;
- resolution is a **lookup**, never a chain of `if caller == ...`.

The reason is concrete. Before function contracts existed, function-dependent rules had
nowhere to live and lodged inside per-argument digesters one branch at a time: 102 of
MolSysMT's 393 digesters branch on `caller`, and the argument contract of a function was
never written in one readable place. A mechanism that forces consumers to write dispatch
logic will grow that shape again.

Declaring rules as data also makes them **readable**: `describe_contract` and
`describe_normalization` render them, so what a function accepts can appear in its own
documentation instead of being a consequence of a branch. A callable would enforce just
as well and document nothing.

## Pattern 6: observable failures

- Raise structured errors with context.
- Keep warning/error messages actionable for integrators.
