# Integration Cheat Sheet

Use this page as a copy-ready reference while integrating ArgDigest.

It is intentionally compact and practical. Use it while coding, then return to
the full User Guide for rationale and migration details.

## Minimum files

```text
mylib/
  _argdigest.py
  basic.py
  _private/digestion/argument/
    selection.py
```

## `_argdigest.py`

```python
DIGESTION_SOURCE = "mylib._private.digestion.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

## Digester file

```python
def digest_selection(selection, caller=None):
    if selection is None:
        return "all"
    if isinstance(selection, str):
        return selection
    raise ValueError(f"Invalid selection in {caller}: {selection!r}")
```

## Decorated function

```python
from argdigest import arg_digest

@arg_digest(config="mylib._argdigest")
def get(molecular_system, selection=None, skip_digestion=False):
    return molecular_system, selection
```

## First tests to run

Start with three checks: `selection=None` is normalized to `"all"`, invalid
`selection` raises an error, and `skip_digestion=True` bypasses digestion when
that path is enabled.

## Immediate benefits

With this minimal integration, you already get shared argument rules across
functions, cleaner business logic with less inline checking, and more
predictable user-facing errors.
