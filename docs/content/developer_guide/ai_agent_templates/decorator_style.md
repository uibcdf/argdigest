# Template: Decorator-style digestion

Use this template when the library prefers to register digesters via `@argument_digest`.

## Goal
- Digesters are registered from any module using the decorator.
- ArgDigest discovers digesters via `digestion_style="decorator"`.

## Required structure
```
my_lib/
  _argdigest.py
  digestion/
    arguments.py
```

## Library config (`my_lib/_argdigest.py`)
```python
DIGESTION_STYLE = "decorator"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

## Digester module (`digestion/arguments.py`)
```python
from argdigest import argument_digest

@argument_digest("selection")
def digest_selection(selection, syntax="MyLib", caller=None):
    if selection is None:
        return "all"
    return selection
```

## Usage in public API
```python
from argdigest import digest

@digest(config="my_lib._argdigest")
def get(molecular_system, selection=None, skip_digestion=False):
    ...
```

## Notes
- This style avoids a fixed directory layout, but you must import the modules that
  register digesters before calling the functions using `@digest`.
