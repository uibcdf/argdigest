# Mixed Migration Strategy

Use this pattern to migrate legacy digestion in controlled slices.

## Context

Many real libraries start with scattered validation code. A full rewrite is risky.
Mixed mode allows gradual migration with minimal disruption.

## Strategy

1. Add `_argdigest.py` with `DIGESTION_STYLE = "auto"`.
2. Keep existing registry digesters active.
3. Introduce new package-style digesters for newly migrated arguments.
4. Use decorator registration for plugin/extension modules.

## `_argdigest.py` example

```python
DIGESTION_SOURCE = [
    "mylib._private.digestion.registry",
    "mylib._private.digestion.argument",
]
DIGESTION_STYLE = "auto"
STRICTNESS = "warn"
```

## Migration checkpoints

- Stage A: warnings are visible and triaged.
- Stage B: no new legacy inline digestion is introduced.
- Stage C: strictness moves from `warn` to `error`.

## When to finish mixed mode

Exit mixed mode when:
- digestion coverage is complete,
- chosen target style is stable,
- migration warnings are resolved in CI.
