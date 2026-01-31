# Template: Mixed style (package + pipelines)

Use this template when the library wants argument digesters **and** pipeline rules.

## Goal
- Argument digesters discovered from a package.
- Pipelines registered by `kind` and referenced in `@digest(map=...)`.

## Required structure
```
my_lib/
  _argdigest.py
  _private/
    digestion/
      argument/
        __init__.py
        selection.py
  pipelines/
    __init__.py
    base.py
```

## Library config (`my_lib/_argdigest.py`)
```python
DIGESTION_SOURCE = "my_lib._private.digestion.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

## Pipeline example (`pipelines/base.py`)
```python
from argdigest import register_pipeline

@register_pipeline(kind="feature", name="feature.base")
def feature_base(obj, ctx):
    if not hasattr(obj, "feature_id"):
        raise ValueError("Missing feature_id")
    return obj
```

## Usage in public API
```python
from argdigest import digest

@digest(
    config="my_lib._argdigest",
    map={"feature": {"kind": "feature", "rules": ["feature.base"]}},
)
def register_feature(feature, skip_digestion=False):
    ...
```
