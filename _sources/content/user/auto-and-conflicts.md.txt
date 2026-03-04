# Auto Mode and Conflict Resolution

`digestion_style="auto"` is useful during migrations and mixed architectures.

## How auto mode is used

Auto mode allows combining sources, for example:

```python
@arg_digest(
    digestion_source=[
        "mylib._private.digestion.registry",
        "mylib._private.digestion.argument",
    ],
    digestion_style="auto",
)
def get(...):
    ...
```

## Conflict scenario

A conflict appears when more than one source defines a digester for the same
argument.

## Recommended policy

Keep one canonical digester per argument whenever possible. During migration,
use source ordering intentionally and document temporary ownership decisions so
contributors understand why a given source wins.

## Migration-safe approach

Start with the legacy source first, then add the new source for migrated
arguments. Move ownership argument by argument, and remove the legacy source
only when migration coverage is complete.

## Warning signs

If the same argument behaves differently across modules, if behavior changes
after small refactors, or if argument-level regressions become frequent, auto
mode likely needs clearer ownership boundaries.

## Next

Continue with [Normalization](normalization.md).
