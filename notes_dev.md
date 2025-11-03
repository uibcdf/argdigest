## Expected behavior

```python
@digest(map={
    "child": {"kind": "feature", "rules": ["feature.base", "feature.shape"]},
    "parent": {"kind": "feature", "rules": ["feature.is_2d"]},
})
def link(child, parent, topo):
    ...
```

## How to use it

In your scientific library (molsysmt/_private/digestion/__init__.py) for instance:

```python
try:
    from argdigest import digest, register_pipeline
except ImportError:
    # no-op substitutes
    def digest(*args, **kwargs):
        def deco(fn):
            return fn
        return deco

    def register_pipeline(*args, **kwargs):
        def deco(fn):
            return fn
        return deco
```

