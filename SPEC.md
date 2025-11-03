---
title: ArgDigest Technical Specification
version: v0.1-draft
authors: [UIBCDF Development Team]
license: MIT
---

# ArgDigest Technical Specification

## 1. Overview

**ArgDigest** provides a unified mechanism for argument coercion, validation, and semantic auditing.  
It exposes a decorator-based API (`@digest`) and a modular pipeline system to register and execute argument validation logic.

### Core goals
- Domain-agnostic core.
- Runtime composition of coercion/validation pipelines.
- Extensible via registry and plugins.
- Standardized error and logging context.

---

## 2. Architecture

```
argdigest/
  core/
    decorator.py
    registry.py
    context.py
    errors.py
    utils.py
  pipelines/
    base_coercers.py
    base_validators.py
  contrib/
    beartype_support.py
    pydantic_support.py
    attrs_support.py
tests/
docs/
```

---

## 3. Core Components

### 3.1 `@digest` decorator

```python
def digest(kind: str = None, rules: list[str] = None):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            ctx = Context.from_function(fn, args, kwargs)
            bound_args = ctx.bound_arguments
            # Execute coercion + validation pipelines
            for arg, config in ctx.arguments_config.items():
                kind = config.get("kind", kind)
                rules = config.get("rules", [])
                Registry.run_pipelines(kind, rules, bound_args[arg], ctx)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
```

### 3.2 `@digest.map` decorator

```python
def map(**kwargs):
    def decorator(fn):
        setattr(fn, "_digest_map", kwargs)
        return digest()(fn)
    return decorator
```

### 3.3 Pipelines and Registry

```python
# registry.py
class Registry:
    _pipelines = {}

    @classmethod
    def register(cls, kind: str, name: str, func):
        cls._pipelines.setdefault(kind, {})[name] = func

    @classmethod
    def run_pipelines(cls, kind, rules, obj, ctx):
        for rule in rules or []:
            func = cls._pipelines[kind].get(rule)
            if func:
                func(obj, ctx)
```

### 3.4 Pipeline decorator

```python
def pipeline(kind: str, name: str = None):
    def decorator(fn):
        Registry.register(kind, name or fn.__name__, fn)
        return fn
    return decorator
```

---

## 4. Error Model

```python
class DigestError(Exception):
    def __init__(self, message, context=None, hint=None):
        super().__init__(message)
        self.context = context
        self.hint = hint

class DigestTypeError(DigestError): pass
class DigestValueError(DigestError): pass
class DigestInvariantError(DigestError): pass
class DigestCoercionWarning(Warning): pass
```

---

## 5. Example: Feature validation in TopoMT

```python
from argdigest import digest, pipeline, Registry

@pipeline(kind="feature", name="rule.mouth_concavity")
def validate_mouth_concavity(obj, ctx):
    if obj.feature_type == "mouth" and ctx.parent.shape_type != "concavity":
        raise DigestInvariantError(
            f"Mouth '{obj.feature_id}' must belong to a concavity.",
            context=ctx,
            hint="Ensure parent feature is of shape_type='concavity'."
        )

@digest.map(
    child={"kind": "feature", "rules": ["rule.mouth_concavity"]},
    parent={"kind": "feature", "rules": ["feature.is_2d"]}
)
def link(child, parent, topo):
    topo.link(child, parent)
```

---

## 6. Example: Molecular system validation in MolSysMT

```python
@digest.map(
    molecular_system={"kind": "molecular_system"},
    selection={"kind": "selection"}
)
def get_n_atoms(molecular_system, selection='all'):
    ...
```

---

## 7. Future extension points
- CLI `argdigest audit script.py`
- Declarative rule sets via YAML/JSONSchema.
- Plugin-based pipeline discovery.
