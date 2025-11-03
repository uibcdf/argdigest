# ArgDigest Developer Guide

## 1. Introduction

ArgDigest is a lightweight toolkit that helps developers enforce **input argument consistency** across scientific Python functions.  
It provides decorators and pipelines that can coerce, validate, and document argument logic.

---

## 2. Core Concepts

### 2.1 Digest Decorator
The `@digest` decorator intercepts function calls, analyzes arguments, and executes **registered pipelines** for coercion and validation.

Example:

```python
from argdigest import digest

@digest(kind="feature")
def register_feature(feature):
    print(f"Registered feature: {feature.feature_id}")
```

### 2.2 Argument Mapping
When a function has multiple arguments, you can assign specific rules per argument:

```python
@digest.map(
    feature={"kind": "feature", "rules": ["feature.base", "shape.consistency"]},
    parent={"kind": "feature", "rules": ["topology.is_2d"]}
)
def link(feature, parent, topo):
    ...
```

---

## 3. Creating Pipelines

A **pipeline** is a function registered for a specific *kind* of argument.  
It receives the argument value (`obj`) and a `context` object containing metadata about the call.

Example:

```python
from argdigest import pipeline

@pipeline(kind="feature")
def coerce_feature(obj, ctx):
    if isinstance(obj, dict):
        # Convert dict to a proper Feature object
        return Feature(**obj)
    return obj

@pipeline(kind="feature", name="shape.consistency")
def validate_shape(obj, ctx):
    if obj.shape_type not in {"concavity", "convexity", "mixed", "boundary"}:
        raise DigestValueError(f"Invalid shape_type: {obj.shape_type}")
```

---

## 4. Error Handling

ArgDigest provides structured exceptions for precise debugging:

```python
from argdigest.errors import DigestError, DigestTypeError

try:
    register_feature(...)
except DigestError as e:
    print(f"Digest error in {e.context.function}:{e.context.argname}")
```

Common error classes:
- `DigestError` — Base class
- `DigestTypeError` — Wrong data type
- `DigestValueError` — Invalid value or domain
- `DigestInvariantError` — Rule violation
- `DigestCoercionWarning` — Non-fatal coercion

---

## 5. Example Integration: TopoMT

```python
from argdigest import digest, pipeline

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

## 6. Example Integration: MolSysMT

```python
@digest.map(
    molecular_system={"kind": "molecular_system"},
    selection={"kind": "selection"}
)
def get_n_atoms(molecular_system, selection='all'):
    ...
```

---

## 7. Extending ArgDigest

You can add custom validators, error messages, or loggers:

```python
from argdigest import registry

@registry.pipeline(kind="feature", name="logger.boundary_link")
def log_feature_link(obj, ctx):
    ctx.logger.info(f"Linking {obj.feature_id} → {ctx.extra.get('parent_id')}")
```

To set a custom logger:

```python
import logging
from argdigest import registry

logger = logging.getLogger("TopoMT.digest")
logger.setLevel(logging.INFO)
registry.set_logger("feature", logger)
```

---

## 8. Minimal Working Example

```python
from dataclasses import dataclass
from argdigest import digest, pipeline, DigestError

@dataclass
class Feature:
    feature_id: str
    shape_type: str
    feature_type: str

@pipeline(kind="feature", name="validate_shape")
def validate_shape(obj, ctx):
    if obj.shape_type not in {"concavity", "convexity"}:
        raise DigestValueError(f"Invalid shape_type: {obj.shape_type}")

@digest(kind="feature", rules=["validate_shape"])
def register_feature(feature):
    print("Registered:", feature.feature_id)

# Usage
f = Feature("f001", "concavity", "pocket")
register_feature(f)
```

---

## 9. Future Directions
- CLI tools for auditing and profiling (`argdigest audit script.py`)
- YAML/JSON declarative rule definitions
- Pydantic and beartype extensions
- Sphinx integration for documentation autogeneration

---

> **ArgDigest** — enabling reusable argument validation pipelines for scientific computing.
