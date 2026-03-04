# Deprecation and Support

This page defines how behavior changes are introduced safely.

## Deprecation principles

- Deprecate before removing.
- Provide a clear replacement path.
- Keep messages actionable and time-bounded.

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
