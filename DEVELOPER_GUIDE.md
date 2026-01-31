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

### 2.3 Science-Aware Context
ArgDigest supports integration with **PyUnitWizard** to manage physical units during digestion:

```python
@digest(puw_context={"standard_units": ["nm", "ps"], "form": "pint"})
def simulation(time):
    ...
```

---

## 3. Creating Pipelines

A **pipeline** is a function registered for a specific *kind* of argument.  
It receives the argument value (`obj`) and a `context` object containing metadata about the call.

**Pro-tip**: You can use **Pydantic models** directly as rules!

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str

@digest.map(user={"kind": "data", "rules": [User]})
def process_user(user):
    # 'user' is now an instance of User
    ...
```

---

## 4. Error Handling

ArgDigest provides structured exceptions for precise debugging. Starting from v0.2, errors include **hints** and **rich context**.

```python
from argdigest import DigestError

try:
    register_feature(...)
except DigestError as e:
    # Print rich error message
    print(e)
    # Access context
    print(f"Failed at: {e.context.function_name}")
```

---

## 5. Minimal Working Example

```python
from pydantic import BaseModel
from argdigest import digest, DigestError

class Feature(BaseModel):
    feature_id: str
    shape_type: str

@digest.map(
    feature={"kind": "feature", "rules": [Feature]},
    type_check=True
)
def register_feature(feature: Feature):
    print("Registered:", feature.feature_id)

# Usage
register_feature({"feature_id": "f001", "shape_type": "concavity"})
```

---

## 6. Future Directions
- CLI tools for auditing (`argdigest audit script.py`)
- YAML/JSON declarative rule definitions (v0.4.0)
- Automatic execution profiling (v0.4.0)
- Advanced Sphinx integration for documentation autogeneration

---

> **ArgDigest** — enabling reusable argument validation pipelines for scientific computing.