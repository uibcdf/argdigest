# Package Style Integration

Use this pattern when you want one digestion module per argument.

## Structure

```text
mylib/
  _argdigest.py
  _private/argdigest/argument/
    selection.py
    syntax.py
    element.py
```

## `_argdigest.py`

```python
DIGESTION_SOURCE = "mylib._private.argdigest.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
FUNCTION_SOURCE = "mylib._private.argdigest.function"
DOMAIN_SOURCE = "mylib._private.argdigest.domain"
NORMALIZATION_SOURCE = "mylib._private.argdigest.normalization"
UNKNOWN_ARGUMENT = "error"
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
4. Call with a mistyped keyword and confirm it is refused, not ignored. A closed
   signature gives you this with nothing declared.
