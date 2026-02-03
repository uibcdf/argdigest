---
title: ArgDigest Technical Specification
version: v0.2
authors: [UIBCDF Development Team]
license: MIT
---

# ArgDigest Technical Specification

## 1. Overview

**ArgDigest** is a lightweight and extensible library for **auditing, validating, and normalizing function arguments** in scientific and analytical Python libraries.

Its purpose is to provide a generic infrastructure that:
- Verifies the **coherence and type** of input arguments.
- **Coerces** heterogeneous objects into the expected internal forms.
- Applies **domain-specific semantic rules** (e.g., topography, molecular systems).
- Produces **consistent and clear error messages** with context and hints.
- Enables **shared and reusable validation pipelines** across different projects (e.g., MolSysMT, TopoMT).

---

## 2. Architecture

The library is structured to separate core logic from domain implementations:

```
argdigest/
  core/
    decorator.py        # Main @arg_digest logic and orchestration
    registry.py         # Pipeline registry (kind/rules)
    argument_registry.py# Argument-centric registry (@argument_digest)
    argument_loader.py  # Discovery logic (packages, modules)
    context.py          # Execution context (function, argname, value)
    errors.py           # Rich exception hierarchy
    logger.py           # Centralized logging
    config.py           # Configuration resolution
    utils.py            # Helper functions (binding, etc.)
  pipelines/            # Built-in generic pipelines
  contrib/              # Integrations (beartype, pydantic)
tests/
docs/
```

---

## 3. Public API

### 3.1 The `@arg_digest` Decorator

The primary entry point is the `@arg_digest` decorator. It supports both **argument-centric discovery** (auto-finding how to digest an argument) and **explicit pipeline mapping**.

```python
@arg_digest(
    # Configuration for Argument-Centric Mode
    digestion_source=None,       # str | list[str]: Module/package paths to search
    digestion_style="auto",      # "auto" | "registry" | "package" | "decorator"
    standardizer=None,           # callable | "module:func": Normalizes arg names
    strictness="warn",           # "warn" | "error" | "ignore": For missing digesters
    skip_param="skip_digestion", # str: Name of param to bypass digestion
    
    # Configuration for Explicit Mode
    map=None,                    # dict: Explicit {arg: {kind, rules}} mapping
    kind=None,                   # str: Default kind for all args (if map is None)
    rules=None,                  # list[str]: Default rules for all args
    
    # Extra config
    config=None                  # str | object: Config object or module path
)
def my_func(...): ...
```

### 3.2 The `@arg_arg_digest.map` Alias

A convenient alias for defining explicit mappings using keyword arguments:

```python
@arg_arg_digest.map(
    arg_name={"kind": "feature", "rules": ["validate_shape"]},
    other_arg={"kind": "topology"}
)
def my_func(arg_name, other_arg): ...
```

### 3.3 Registration Decorators

- **`@argument_digest(arg_name)`**: Registers a function to digest a specific argument name globally (used in `digestion_style="decorator"`).
- **`@register_pipeline(kind, name)`**: Registers a reusable pipeline function (coercer/validator) for a specific semantic kind.

---

## 4. Digestion Logic & Behavior

### 4.1 Argument-Centric Discovery
When `digestion_source` or `digestion_style` is used, ArgDigest attempts to find a "digester" function for each argument.

**Discovery Styles:**
- **`registry`**: Looks for an `ARGUMENT_DIGESTERS` dictionary in the `digestion_source` module.
- **`package`**: Scans the `digestion_source` package for functions named `digest_<arg_name>`.
- **`decorator`**: Uses the global registry built by `@argument_digest`.
- **`auto`**: Tries `registry` → `package` → `decorator` in order, merging results.

**Behavior Contracts:**
1.  **Skip**: If `skip_param=True` is passed to the function, **all digestion is skipped**.
2.  **Execution**:
    - If a digester is found, it is executed. The digester receives the raw value and can request other arguments (dependency injection).
    - If no digester is found, `strictness` determines the action (`warn`, `error`, or `ignore`).
3.  **Result**: The original function is called with the *transformed* values.

### 4.2 Dependency Resolution
Digesters can declare dependencies on other arguments.
- ArgDigest resolves the execution order (topological sort).
- **Cycles**: If a cycle is detected (e.g., `a` needs `b`, `b` needs `a`), a `DigestNotDigestedError` is raised with the full cycle path (e.g., `a -> b -> a`).

### 4.3 Hooks
- **Standardizer**: Runs *before* digestion. It normalizes argument names (e.g., converting aliases like `sel` to `selection`) so that digesters match correctly.

---

## 5. Error Model

Exceptions are rich objects inheriting from `DigestError`. They include:
- `message`: Human-readable description.
- `context`: A `Context` or `SimpleNamespace` object containing:
    - `function_name`: Where the error occurred.
    - `argname`: The specific argument involved.
    - `value`: The runtime value (truncated representation).
- `hint`: Actionable advice for the user.

**Hierarchy:**
- `DigestError`
  - `DigestTypeError`: Type mismatch.
  - `DigestValueError`: Semantic validation failure.
  - `DigestInvariantError`: Multi-argument rule violation.
  - `DigestNotDigestedError`: Missing digester (when strictness="error") or cyclic dependency.

---

## 6. Compatibility Profiles

### 6.1 MolSysMT Profile
Recommended configuration for MolSysMT integration:

```python
@arg_digest(
    digestion_source="molsysmt._private.digestion.argument",
    digestion_style="package",
    standardizer="molsysmt._private.digestion.argument_names_standardization",
    skip_param="skip_digestion",
    strictness="warn"
)
```

---

## 7. Examples

### Explicit Mapping
```python
from argdigest import arg_digest, register_pipeline

@register_pipeline(kind="feature", name="is_2d")
def check_2d(val, ctx):
    if val.dim != 2: raise ValueError("Not 2D")
    return val

@arg_arg_digest.map(
    surface={"kind": "feature", "rules": ["is_2d"]}
)
def calculate_area(surface):
    ...
```

### Argument-Centric (Package Style)
File: `mylib/_private/digestion.py`
```python
def digest_volume(volume, caller=None):
    return float(volume)
```

File: `mylib/api.py`
```python
@arg_digest(digestion_source="mylib._private.digestion", digestion_style="package")
def compute(volume):
    # volume is guaranteed to be float here
    ...
```