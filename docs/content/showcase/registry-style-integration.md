# Registry Style Integration

Use this pattern when your team prefers a central explicit map.

## Structure

```text
mylib/
  _argdigest.py
  _private/argdigest/
    registry.py
    digesters.py
```

## Registry module

```python
# mylib/_private/argdigest/registry.py
from .digesters import digest_selection, digest_syntax

ARGUMENT_DIGESTERS = {
    "selection": digest_selection,
    "syntax": digest_syntax,
}
```

## `_argdigest.py`

```python
DIGESTION_SOURCE = "mylib._private.argdigest.registry"
DIGESTION_STYLE = "registry"
STRICTNESS = "error"
FUNCTION_SOURCE = "mylib._private.argdigest.function"
DOMAIN_SOURCE = "mylib._private.argdigest.domain"
NORMALIZATION_SOURCE = "mylib._private.argdigest.normalization"
UNKNOWN_ARGUMENT = "error"
```

## Decorated function

```python
from argdigest import arg_digest

@arg_digest(config="mylib._argdigest")
def select(selection=None, syntax="MolSysMT"):
    ...
```

## Why this style works

- Single discovery surface for all active digesters.
- Easy audit of digestion coverage by argument name.
- Good fit for medium-size APIs with centralized maintenance.

4. Call with a mistyped keyword and confirm it is refused, not ignored. A closed
   signature gives you this with nothing declared.
