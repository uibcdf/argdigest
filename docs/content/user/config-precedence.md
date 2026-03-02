# Configuration Precedence

This page defines the exact precedence used by ArgDigest.

## Resolution order

ArgDigest resolves configuration from most specific to most general. Decorator
arguments in `@arg_digest(...)` have highest priority. Then comes an explicit
`config=` module/object, followed by auto-discovery of
`<root_package>._argdigest` when no explicit config is provided. If none of that
is available, ArgDigest uses global defaults from
`argdigest.config.set_defaults(...)`, and finally built-in defaults.

## Practical examples

### Example A: decorator override wins

```python
@arg_digest(config="mylib._argdigest", strictness="error")
def get(...):
    ...
```

If `mylib._argdigest` sets `STRICTNESS = "warn"`, the effective value is `error`.

### Example B: explicit config beats auto-discovery

```python
@arg_digest(config="mylib.custom_argdigest")
def get(...):
    ...
```

ArgDigest does not use `<root_package>._argdigest` for this function.

### Example C: no explicit config

```python
@arg_digest()
def get(...):
    ...
```

ArgDigest tries `<root_package>._argdigest`. If unavailable, global defaults apply.

## Recommendation

In production libraries, a good default is to keep most functions on
`@arg_digest(config="mylib._argdigest")` and reserve decorator-level overrides
for exceptional endpoints. Too many local overrides make behavior harder to
reason about and slower to review.

## Next

Continue with [Digestion Styles](digestion-styles.md).
