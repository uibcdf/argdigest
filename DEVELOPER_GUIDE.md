# ArgDigest Developer Guide

## 1. Introduction

ArgDigest is a lightweight toolkit that helps developers enforce **input argument consistency** across scientific Python functions.  
It provides decorators and pipelines that can coerce, validate, and document argument logic.

---

## 2. Core Concepts

### 2.1 Digest Decorator
The `@arg_digest` decorator intercepts function calls, analyzes arguments, and executes **registered pipelines** for coercion and validation.

### 2.2 Argument Mapping
When a function has multiple arguments, you can assign specific rules per argument:

```python
arg_digest.map(
    feature={"kind": "feature", "rules": ["feature.base", "shape.consistency"]},
    parent={"kind": "feature", "rules": ["topology.is_2d"]}
)
def link(feature, parent, topo):
    ...
```

### 2.3 Science-Aware Context
ArgDigest supports integration with **PyUnitWizard** to manage physical units during digestion:

```python
@arg_digest(puw_context={"standard_units": ["nm", "ps"], "form": "pint"})
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

arg_digest.map(user={"kind": "data", "rules": [User]})
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

## 4.1 smonitor Integration

ArgDigest uses a catalog-driven integration with smonitor:
- `argdigest/_smonitor.py` defines profiles and runtime settings.
- `argdigest/_private/smonitor/catalog.py` contains CODES/SIGNALS.
- `argdigest/_private/smonitor/meta.py` stores docs/issues URLs (if any).

---

## 5. CLI Tools for Agents & Developers

ArgDigest provides command-line tools to help both humans and AI agents:

```bash
# Audit a module to see all applied rules
argdigest audit my_lib.api

# Generate context instructions for AI Agents
argdigest agent init --module my_lib
```

---

## 6. Quality Assurance (Pre-Release Checklist)

Before submitting a Pull Request, creating a Tag, or releasing a new version, you **MUST** ensure the following:

1.  **Functional Tests**: Run all tests and ensure they pass.
    ```bash
    export PYTHONPATH=.
    pytest tests/
    ```
2.  **Code Style (Linting)**: Run `ruff` to ensure compliance with style standards.
    ```bash
    ruff check .
    ```
3.  **No unused imports**: Pay special attention to `sys` or `Any` imports which are common linting failures.

**Motto**: *If tests pass but linter fails, the build is RED.* 🔴

---

## 7. Minimal Working Example

```python
from pydantic import BaseModel
from argdigest import arg_digest, DigestError

class Feature(BaseModel):
    feature_id: str
    shape_type: str

arg_digest.map(
    feature={"kind": "feature", "rules": [Feature]},
    type_check=True
)
def register_feature(feature: Feature):
    print("Registered:", feature.feature_id)

# Usage
register_feature({"feature_id": "f001", "shape_type": "concavity"})
```

---

## 8. Future Directions
- CLI tools for auditing (`argdigest audit script.py`)
- YAML/JSON declarative rule definitions (v0.4.0)
- Automatic execution profiling (v0.4.0)
- Advanced Sphinx integration for documentation autogeneration

---

> **ArgDigest** — enabling reusable argument validation pipelines for scientific computing.
