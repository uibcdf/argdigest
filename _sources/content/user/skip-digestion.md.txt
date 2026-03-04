# skip_digestion Behavior

ArgDigest supports an optional bypass parameter to skip digestion at call time.

This mechanism is useful, but it should be treated as a controlled exception to
normal behavior, not as the default usage pattern.

## Typical setup

```python
@arg_digest(config="mylib._argdigest")
def get(molecular_system, selection=None, skip_digestion=False):
    ...
```

with:

```python
# mylib/_argdigest.py
SKIP_PARAM = "skip_digestion"
```

## What happens when bypass is enabled

When bypass is enabled, argument digesters and pipeline rules are both skipped,
so raw function arguments flow directly into your function logic.

## Safe usage guidance

Use bypass only for:
- internal debug scenarios,
- migration bridges,
- controlled performance probes.

In most libraries, bypass should not be exposed as a default public behavior for
end users, because it weakens the consistency guarantees of the API boundary.

## Testing recommendation

When bypass exists, test both paths:
1. default path (digestion on),
2. bypass path (digestion off).

This two-path testing is important: it prevents bypass behavior from drifting
silently as digestion logic evolves.

## Next

Continue with [Pipeline Design Patterns](pipeline-design.md).
