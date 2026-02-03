---
title: ArgDigest — Argument Auditing and Normalization Library
version: v0.1-draft
authors: [UIBCDF Development Team]
license: MIT
---

# ArgDigest — Argument Auditing and Normalization Library

## 🧩 Project Definition

**ArgDigest** is a lightweight and extensible library for **auditing, validating, and normalizing function arguments** in scientific and analytical Python libraries.

Its purpose is to provide a generic infrastructure that:
- Verifies the **coherence and type** of input arguments.
- **Coerces** heterogeneous objects into the expected internal forms.
- Applies **domain-specific semantic rules** (e.g., topography, molecular systems).
- Produces **consistent and clear error messages and warnings**.
- Enables **shared and reusable validation pipelines** across different projects (MolSysMT, TopoMT, etc.).

ArgDigest originates from the `@digest` decorator developed for **MolSysMT** and later adopted by **TopoMT**, now refactored into an independent, documented, and stable standalone project.

---

## ⚙️ Core Objectives

1. **Domain-agnostic core**
   - Make no assumptions about molecular, topographic, or other data structures.
   - Orchestrate configurable *coercion* and *validation* pipelines identified by `kind` and `rules`.

2. **Modular extensibility**
   - Each user library (e.g., MolSysMT, TopoMT) defines its own semantic rules:
     - **Coercion and validation pipelines** via `@pipeline`.
     - **Contracts and valid domains** (e.g., `shape_type`, `feature_type`, `selection_type`).
     - **Custom messages, hints, and exceptions**.
     - **Domain-specific loggers** integrated into the ArgDigest execution context.
   - ArgDigest provides only the **infrastructure** to execute, register, and compose these pipelines,
     without imposing scientific semantics or specific data models.
   - Each library can register its pipelines dynamically using the global `registry`
     or through autodiscoverable *plugins*.

3. **Modern typing integration**
   - Full compatibility with `TypeAlias`, `Literal`, and `Protocol`.
   - Optional runtime enforcement via `beartype` or `pydantic`.

4. **Messaging and traceability**
   - Unified error system with contextual information: function, argument, value, and hint.
   - Optional logging and “profiling mode” for runtime audits.

5. **Decoupled and performant**
   - Zero-dependency core (`typing`, `inspect`, `dataclasses` only).
   - Optional `contrib/` extensions for advanced ecosystems (beartype, pydantic, attrs).

---

## 🏗️ Initial Package Structure

```
argdigest/
  __init__.py
  core/
    decorator.py        # implements @digest and @digest.map
    registry.py         # global pipeline and validator registry
    context.py          # call context (function, argname, value, metadata)
    errors.py           # standardized exception hierarchy
    utils.py            # argument binding and helper functions
  pipelines/
    base_coercers.py    # generic coercers (dict→obj, lowercase normalization, etc.)
    base_validators.py  # simple validators (type checks, domain enforcement, uniqueness)
  contrib/
    beartype_support.py # optional integration with beartype
    pydantic_support.py # optional integration with pydantic v2
    attrs_support.py    # optional integration with attrs/cattrs
tests/
  ...
docs/
  index.md
  api_reference.md
  examples/
```

---

## 🔧 Core API (Concept Draft)

### Basic decorator

```python
from argdigest import digest

@digest(kind="feature")
def register_feature(feature):
    ...
```

### Decorator with argument mapping

```python
@digest.map(
    feature={"kind": "feature", "rules": ["feature.base", "shape.consistency"]},
    parent={"kind": "feature", "rules": ["topology.is_2d"]}
)
def link(feature, parent, topo):
    ...
```

### Pipeline registration

```python
from argdigest import registry, pipeline

@pipeline(kind="feature")
def coerce_feature(obj, ctx):
    """Convert a dict or dataclass into a valid Feature object."""
    ...

@pipeline(kind="feature", name="topology.shape_consistency")
def validate_shape(obj, ctx):
    """Validate shape_type and dimensionality consistency."""
    ...
```

---

## 🧱 Error Hierarchy

| Class | Description |
|:--|:--|
| `DigestError` | Base class for all ArgDigest exceptions. |
| `DigestTypeError` | Unexpected or inconsistent data type. |
| `DigestValueError` | Invalid or out-of-domain value. |
| `DigestInvariantError` | Semantic rule violation (e.g., invalid parent-child link). |
| `DigestCoercionWarning` | Automatic or silent coercion warning. |

Each exception includes:
- `context.function`: function name where the issue occurred.
- `context.argname`: argument name.
- `context.value_repr`: summarized representation of the value.
- `hint`: suggestion or cause explanation.

---

## 🔌 Ecosystem Integrations

| Integration | Purpose |
|:-------------|:-----------|
| **beartype** | Enforce typing annotations at runtime (optional). |
| **pydantic v2** | Validate and parse DTOs (external inputs). |
| **attrs/cattrs** | Fast dict↔object conversions for pipelines. |
| **numpy/pandas** (future) | Coercion of arrays and tabular data to validated sequences. |

---

## ⚙️ Example usage in scientific libraries

### In MolSysMT
```python
@digest.map(
    molecular_system={"kind": "molecular_system"},
    selection={"kind": "selection"}
)
def get_n_atoms(molecular_system, selection='all'):
    ...
```

### In TopoMT
```python
@digest.map(
    child={"kind": "feature", "rules": ["parent_child.mouth_concavity"]},
    parent={"kind": "feature", "rules": ["is_2d"]}
)
def link(child, parent, topo):
    ...
```

---

## 🧭 Development Roadmap

| Phase | Objectives | Deliverables |
|:------|:-----------|:-------------|
| **v0.1 (Prototype)** | Functional `@digest` decorator + minimal registry | **Done**: Core pipeline, argument-centric mode, `@digest.map` |
| **v0.2.0** | Context-aware error system + logging | **Done**: Rich exceptions, logging, native Pydantic/Beartype |
| **v0.3.0** | Standard Pipelines & Science Integration | **Done**: Built-in pipelines, PyUnitWizard integration, legacy compat |
| **v0.4.0** | Declarative Config & Advanced Features | **Done**: YAML/JSON rules, Numpy/Pandas support, Profiling |
| **v0.5.0** | Performance & CLI Tooling | **Done**: Digestion Plan Caching, CLI Audit & Agent tools, LRU Caching for Package Loader |
| **v0.6.0** | Pilot Integration (MolSysMT) | Replace legacy engine in MolSysMT key modules |
| **v1.0.0** | Stable API + >90% coverage + Release | 1.0.0 release, full CI/CD, PyPI/Conda distribution |

---

## 📦 Distribution and License

- **Package name**: `argdigest`
- **License**: MIT License (consistent with UIBCDF ecosystem).
- **GitHub repository**: `uibcdf/argdigest`
- **Distribution**:
  - `PyPI` (wheels and sdist)
  - `conda-forge` (meta.yaml with tests)
- **CI/CD**:
  - GitHub Actions: lint (ruff), type-check (mypy/pyright), test (pytest), build/publish.
  - Codecov: minimum 85% coverage.

---

## 💡 Future Ideas

- **Profiling mode**: runtime collection of coercion and validation statistics.
- **Declarative validation** (`YAML`/`JSONSchema` → pipelines).
- **Sphinx integration**: automatic documentation of validation logic.
- **Undo/revert hooks** for reversible coercions.
- **CLI audit tool** (`argdigest audit script.py`).

---

## ✨ Tagline

> **ArgDigest** — the lightweight, extensible toolkit to audit, coerce, and validate function arguments across scientific libraries.
