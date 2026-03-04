# Mini Library Walkthrough

This walkthrough shows a complete, small integration using package-style digesters
and library-level defaults in `_argdigest.py`.

## Project layout

```text
mylib/
  __init__.py
  _argdigest.py
  basic.py
  _private/
    digestion/
      argument/
        __init__.py
        selection.py
        syntax.py
```

## 1. Define library defaults

```python
# mylib/_argdigest.py
DIGESTION_SOURCE = "mylib._private.digestion.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

## 2. Define digesters

```python
# mylib/_private/digestion/argument/selection.py
def digest_selection(selection, syntax="MolSysMT", caller=None):
    if selection is None:
        return "all"
    if isinstance(selection, str):
        return selection
    if syntax == "MolSysMT" and isinstance(selection, int):
        return [selection]
    raise ValueError(f"Invalid selection in {caller}: {selection!r}")
```

```python
# mylib/_private/digestion/argument/syntax.py
def digest_syntax(syntax, caller=None):
    if syntax is None:
        return "MolSysMT"
    if isinstance(syntax, str):
        return syntax
    raise ValueError(f"Invalid syntax in {caller}: {syntax!r}")
```

## 3. Decorate API functions

```python
# mylib/basic.py
from argdigest import arg_digest

@arg_digest(config="mylib._argdigest")
def get(molecular_system, selection=None, syntax=None, skip_digestion=False):
    return molecular_system, selection, syntax
```

## 4. Add one pipeline rule (optional)

```python
from argdigest import register_pipeline

@register_pipeline(kind="selection", name="selection.non_empty")
def selection_non_empty(value, ctx):
    if value == "":
        raise ValueError("selection cannot be empty")
    return value
```

Then attach it in `@arg_digest(map={...})` where needed.

## Expected result

- `selection` and `syntax` are digested before function logic executes.
- The integration remains localized in digestion modules, not spread across API code.
- Additional rules can be layered via pipelines without changing digesters.

## Next

Continue with [Configuration](configuration.md).
