# Package Style Integration

Use this pattern when you want one digestion module per argument.

## Structure

```text
mylib/
  _argdigest.py
  _private/digestion/argument/
    selection.py
    syntax.py
    element.py
```

## `_argdigest.py`

```python
DIGESTION_SOURCE = "mylib._private.digestion.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
```

## Decorated function

```python
from argdigest import arg_digest

@arg_digest(config="mylib._argdigest")
def get(molecular_system, element=None, selection=None, syntax=None):
    ...
```

## Why this style works

- Digestion logic stays modular and reviewable.
- Each argument has a natural ownership boundary.
- It maps well to scientific libraries with many semantic arguments.

## Smoke check

1. Call a function with valid input and confirm normalization.
2. Call with invalid input and confirm digestion error with context.
3. Call with aliases and confirm standardization behavior (if configured).
