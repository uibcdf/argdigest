# Decorator Style Integration

Use this pattern when digestion logic should stay next to API code.

## Structure

```text
mylib/
  api.py
```

## Co-located digesters

```python
from argdigest import arg_digest, argument_digest


@argument_digest("selection")
def digest_selection(selection, syntax="MolSysMT", caller=None):
    if selection is None:
        return "all"
    return str(selection)


@argument_digest("syntax")
def digest_syntax(syntax, caller=None):
    if syntax is None:
        return "MolSysMT"
    return str(syntax)
```

## Decorated function

```python
@arg_digest(digestion_style="decorator", strictness="error")
def get(molecular_system, selection=None, syntax="MolSysMT"):
    return molecular_system, selection, syntax
```

## Why this style works

- Digesters are versioned with the same module as the API function.
- Refactors are simple because digesters move with the function.
- Plugin modules can register additional digesters without touching package registries.

## Smoke check

1. call with `selection=None` and verify default normalization.
2. call with explicit `syntax` and verify no warning/error noise.
3. call with malformed values and verify catalog-backed digest errors.
