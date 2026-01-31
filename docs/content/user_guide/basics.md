# Basics

ArgDigest wraps functions with a `@digest` decorator that can:

1) Digest individual arguments using **argument-centric digesters**.
2) Apply reusable **pipelines** by `kind` and `rules`.

## Argument-centric digestion

```python
from argdigest import digest, argument_digest

@argument_digest("selection")
def digest_selection(selection, caller=None, syntax=None):
    if selection is None:
        return "all"
    return selection

@digest(digestion_style="decorator", strictness="warn")
def get(molecular_system, selection=None, skip_digestion=False):
    return molecular_system, selection
```

## Pipeline-based validation

```python
from argdigest import digest, register_pipeline

@register_pipeline(kind="feature", name="feature.base")
def feature_base(obj, ctx):
    if not hasattr(obj, "feature_id"):
        raise ValueError("Missing feature_id")
    return obj

@digest(map={"feature": {"kind": "feature", "rules": ["feature.base"]}})
def register_feature(feature):
    return feature
```

## Dual mode (argument digestion + pipelines)

If both are configured, argument digestion runs **first**, then pipelines are applied to the
updated values.

## Library-level defaults

To avoid repeating `digestion_source` and `digestion_style` in every decorator, a library can
define a configuration module (for example `mylib/_argdigest.py`) and reference it via `config`.

```python
# mylib/_argdigest.py
DIGESTION_SOURCE = "mylib._private.digestion.argument"
DIGESTION_STYLE = "package"
STANDARDIZER = "mylib._private.digestion.argument_names_standardization:argument_names_standardization"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

```python
from argdigest import digest

@digest(config="mylib._argdigest")
def myfunc(...):
    ...
```

If `@digest()` is used without explicit configuration, ArgDigest will try to auto-discover
`<root_package>._argdigest` based on the decorated function's module. If not found, the
global defaults are used.
