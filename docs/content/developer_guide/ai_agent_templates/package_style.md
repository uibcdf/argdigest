# Template: Package-style digestion

Use this template when the library will store one digester per argument under a package.

## Goal
- Each argument has a file `digest_<argument>` in `_private/digestion/argument/`.
- ArgDigest discovers digesters via `digestion_style="package"`.

## Required structure
```
my_lib/
  _argdigest.py
  _private/
    digestion/
      argument/
        __init__.py
        selection.py
        atom_index.py
      normalization/
        __init__.py
        standardizer.py
```

## Library config (`my_lib/_argdigest.py`)
```python
DIGESTION_SOURCE = "my_lib._private.digestion.argument"
DIGESTION_STYLE = "package"
STANDARDIZER = "my_lib._private.digestion.normalization.standardizer:standardizer"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

## Digester template (`selection.py`)
```python
def digest_selection(selection, syntax="MyLib", caller=None):
    if selection is None:
        return "all"
    if isinstance(selection, str):
        return selection
    if isinstance(selection, int):
        return [selection]
    raise ArgumentError("selection", value=selection, caller=caller, message=None)
```

## Usage in public API
```python
from argdigest import digest

@digest(config="my_lib._argdigest")
def get(molecular_system, selection=None, syntax="MyLib", skip_digestion=False):
    ...
```

## Notes
- If `@digest()` is used without `config`, ArgDigest auto-detects `my_lib._argdigest`.
- Digesters can depend on other arguments (e.g., `syntax`) and ArgDigest resolves them.
