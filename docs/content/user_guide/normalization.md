# Normalization

Some libraries need to normalize argument names before digestion (for example, mapping
synonyms or resolving context-specific names).

ArgDigest supports an optional **standardizer** hook:

```python
from argdigest import arg_digest

def standardizer(caller, kwargs):
    if caller.endswith(".get") and "name" in kwargs:
        kwargs = dict(kwargs)
        kwargs["element_name"] = kwargs.pop("name")
    return kwargs

@arg_digest(standardizer=standardizer, strictness="warn")
def get(element_name=None, **kwargs):
    return element_name
```

The standardizer receives `(caller, kwargs)` and must return a new kwargs dict.
It runs before any digestion.

## Modular normalization

For larger libraries, it is useful to split normalization into layers:

- **Declarative aliases** per caller (simple renames).
- **Global aliases** shared across the library.
- **Dynamic rules** for caller-specific logic (for example, `element + "_name"`).

A simple pattern is:

```
mylib/_private/digestion/normalization/
  __init__.py
  aliases.py
  caller_rules.py
  dynamic_rules.py
  standardizer.py
```

This keeps the dynamic logic contained while leaving most rules declarative.

### Dynamic rule example

```python
# dynamic_rules.py
def normalize_get(caller, kwargs):
    if "name" in kwargs and "element" in kwargs:
        kwargs = dict(kwargs)
        kwargs[f"{kwargs['element']}_name"] = kwargs.pop("name")
    return kwargs

CALLER_DYNAMIC = {
    "mylib.basic.get.get": normalize_get,
}
```
