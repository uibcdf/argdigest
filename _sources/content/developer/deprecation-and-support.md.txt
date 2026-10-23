# Deprecation and Support

This page defines how behavior changes are introduced safely.

## Deprecation principles

- Deprecate before removing.
- Provide a clear replacement path.
- Keep messages actionable and time-bounded.

## 0.10.0: one deliberate breaking change

`unknown_argument` defaults to `error`, so a keyword outside a function's contract is
refused instead of silently discarded.

It was taken before `1.0.0` rather than after, by explicit release-owner decision,
because ArgDigest was **more permissive than the language it wraps**: plain Python raises
`TypeError` for an unexpected keyword and a decorated function accepted it. Stabilizing
`1.0.0` on top of that would have frozen the anomaly into the contract every downstream
library then depends on.

It was not deprecated first because there was nothing to deprecate: no API was removed or
renamed, and the previous behaviour was the defect. The escape hatch is configuration
rather than a deprecation cycle — `UNKNOWN_ARGUMENT = "warn"` or `"ignore"` restores it.

Two properties bound the blast radius: a closed signature is held to its own parameters,
which only refuses calls that were already wrong; and a function with `**kwargs` admits
anything until its domain is declared, so no library is broken by a declaration it has
not written. Both first-party consumers passed with no change on their side.

## 0.7.x status

- No breaking deprecations are currently planned before `1.0.0`.
- If a deprecation becomes necessary during `0.7.x`, it must:
  1. be announced in release notes,
  2. include migration guidance,
  3. remain in place for at least one minor release window before removal.

## Recommended deprecation flow

1. Introduce replacement behavior.
2. Emit deprecation warning in old path.
3. Update docs and examples.
4. Remove deprecated path only after documented support window.

## Support scope

ArgDigest support prioritizes:
- documented public API,
- documented integration styles,
- documented configuration resolution behavior.

## Diagnostics rule

Deprecation diagnostics must be emitted through catalog-backed warning paths
(SMonitor integration), not through ad-hoc hardcoded strings.
