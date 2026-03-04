# Normalization

Normalization standardizes argument names before digestion runs.

Use it when a function accepts aliases (`name` vs `atom_name`) or when argument
meaning depends on another argument (`element` + `name`).

## Standardizer hook

ArgDigest supports an optional `standardizer` callable:

```python
from argdigest import arg_digest

def argument_names_standardization(caller, kwargs):
    if caller.endswith(".get") and "name" in kwargs:
        kwargs = dict(kwargs)
        kwargs["element_name"] = kwargs.pop("name")
    return kwargs

@arg_digest(standardizer=argument_names_standardization, strictness="warn")
def get(element_name=None, **kwargs):
    return element_name
```

Contract:
- input: `(caller, kwargs)`,
- output: normalized kwargs dictionary.

Normalization runs before any argument digester.

## Recommended modular layout

```text
mylib/_private/digestion/normalization/
  aliases.py
  caller_rules.py
  dynamic_rules.py
  standardizer.py
```

Suggested responsibilities:
- `aliases.py`: global and local static aliases.
- `caller_rules.py`: caller-specific rename tables.
- `dynamic_rules.py`: conditional rules using runtime context.
- `standardizer.py`: orchestration entry point used by ArgDigest.

## Dynamic rule example (`name` + `element`)

```python
def normalize_get(caller, kwargs):
    if "name" in kwargs and "element" in kwargs:
        kwargs = dict(kwargs)
        kwargs[f"{kwargs['element']}_name"] = kwargs.pop("name")
    return kwargs
```

This pattern covers cases like:
- if `element="atom"` and `name="CA"`, produce `atom_name="CA"`.

## Next

Continue with [skip_digestion Behavior](skip-digestion.md).
