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
PUW_CONTEXT = {"standard_units": ["nm", "ps"]} # Optional: for Science libraries
```

## Programmatic config alternative (`my_lib/__init__.py`)
```python
import argdigest.config

argdigest.config.set_defaults(
    digestion_source="my_lib._private.digestion.argument",
    digestion_style="package",
    strictness="warn"
)
```

## Digester template (`selection.py`)
```python
def digest_selection(selection, syntax="MyLib", caller=None):
    # Use standard pipelines internally if needed
    # from argdigest.pipelines.coercers import to_list
    # selection = to_list(selection)
    
    if selection is None:
        return "all"
    ...
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
