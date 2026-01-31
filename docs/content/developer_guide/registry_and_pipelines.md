# Registry and pipelines

## Pipeline registry

Pipelines are registered by `kind` and `name`.

```python
from argdigest import register_pipeline

@register_pipeline(kind="feature", name="feature.base")
def feature_base(obj, ctx):
    if not hasattr(obj, "feature_id"):
        raise ValueError("Missing feature_id")
    return obj
```

## Argument digester registry

Argument digesters can be registered with a decorator:

```python
from argdigest import argument_digest

@argument_digest("selection")
def digest_selection(selection, caller=None, syntax=None):
    return selection
```

Alternatively, digesters can be discovered from a module or package by name
(`digest_<argument>`).
