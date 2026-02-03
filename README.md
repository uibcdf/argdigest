# ArgDigest

**ArgDigest** is a lightweight and extensible Python library for **auditing, validating, and normalizing function arguments** in scientific and analytical libraries.

It provides a unified infrastructure to:
- Verify the **coherence and type** of input arguments.
- **Coerce** heterogeneous objects into expected internal forms (e.g., strings to lists, dicts to Pydantic models).
- Apply **domain-specific semantic rules** (e.g., physical dimensions, molecular system checks).
- Produce **consistent and clear error messages** with context and hints.
- Enable **shared and reusable validation pipelines**.

---

## 🚀 Quick Start

### Installation

```bash
pip install argdigest[all]  # Includes Pydantic, Beartype, and PyUnitWizard support
```

### Basic Usage: Explicit Mapping

Use `arg_digest.map` to define validation rules for specific arguments:

```python
from argdigest import arg_digest
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

arg_digest.map(
    # Use standard rules
    flag={"kind": "std", "rules": ["to_bool"]},
    # Native Pydantic model validation
    user={"kind": "data", "rules": [User]}
)
def register_user(flag, user):
    return flag, user

register_user("yes", {"name": "Diego", "age": 30})
# Output: (True, User(name='Diego', age=30))
```

### Advanced: Science-Aware Validation

Integrate with `PyUnitWizard` for physical quantities:

```python
from argdigest import arg_digest
from argdigest.contrib import pyunitwizard_support as puw_support

arg_digest.map(
    puw_context={"standard_units": ["nm", "ps"]}, # Temporary unit system
    cutoff={
        "kind": "quantity", 
        "rules": [
            puw_support.check(dimensionality={'[L]': 1}), # Must be length
            puw_support.standardize()                     # Convert to nm
        ]
    }
)
def compute(cutoff):
    return cutoff
```

### CLI Tools for Agents & Developers

ArgDigest provides command-line tools to help both humans and AI agents understand the validation rules of a project.

```bash
# Audit a module to see all applied rules
argdigest audit my_lib.api

# Generate context instructions for AI Agents
argdigest agent init --module my_lib
```

---

## 🛠️ Key Features

- **Argument-Centric Discovery**: Automatically find digesters in your package structure.
- **Native Integrations**: First-class support for **Pydantic** (v2) and **Beartype** (O(1) type checking).
- **Batteries Included**: Built-in standard pipelines (`to_list`, `to_bool`, `is_file`, etc.).
- **Rich Diagnostics**: Detailed error messages including function name, argument name, and value context.
- **Legacy Compatible**: Designed to replace and improve the MolSysMT digestion engine.

---

## 📖 Documentation

Full documentation is available at [uibcdf.org/argdigest](https://uibcdf.org/argdigest).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.