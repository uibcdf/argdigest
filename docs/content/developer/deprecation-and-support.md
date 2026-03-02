# Deprecation and Support

This page defines how behavior changes are introduced safely.

## Deprecation principles

- Deprecate before removing.
- Provide a clear replacement path.
- Keep messages actionable and time-bounded.

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
