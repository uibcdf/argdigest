# Implementation Patterns

These patterns help evolve ArgDigest without breaking downstream integrations.

## Pattern 1: contract-first evolution

- Define expected behavior before implementation changes.
- Keep documentation and tests aligned with contract decisions.

## Pattern 2: explicit precedence

When adding new configuration behaviors, keep precedence stable:
1. decorator arguments,
2. explicit config module,
3. auto-discovery defaults.

## Pattern 3: migration-safe defaults

- Prefer non-breaking defaults in minor versions.
- Introduce stricter behavior behind explicit options first.

## Pattern 4: architecture freedom for adopters

Do not force one digestion layout. Preserve support for:
- package style,
- registry style,
- decorator style,
- mixed mode.

## Pattern 5: observable failures

- Raise structured errors with context.
- Keep warning/error messages actionable for integrators.
