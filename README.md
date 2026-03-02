# ArgDigest

**ArgDigest** is a Python library for **digesting function arguments** at API boundaries.
It helps libraries normalize, validate, and standardize inputs with explicit,
reusable contracts.

It combines:
- **Argument-centric digestion** (per-argument digesters),
- **Pipeline rules** (reusable validation/coercion by kind and rule name),
- **Structured diagnostics** (clear warnings and errors with context).

---

## 🚀 Quick Start

### Installation

```bash
pip install argdigest[all]  # Includes Pydantic, Beartype, and PyUnitWizard support
```

### Basic usage: digesters + pipelines

```python
from argdigest import arg_digest

@arg_digest(
    digestion_source="mylib._private.digestion.argument",
    digestion_style="package",
    strictness="warn",
    map={"syntax": {"kind": "std", "rules": ["is_str"]}},
)
def get(molecular_system, selection=None, syntax="MolSysMT"):
    return molecular_system, selection, syntax
```

### Alternate styles

- `package`: one module per argument (`digest_<argument>`),
- `registry`: central `ARGUMENT_DIGESTERS` mapping,
- `decorator`: registration via `@argument_digest("arg")`,
- `auto`: mixed mode for incremental migrations.

---

## 🛠️ Key Features

- Package/registry/decorator/mixed digestion styles.
- Standardizer hook for argument-name normalization.
- Strictness modes (`warn`, `error`, `ignore`).
- Reusable pipeline registry by `kind` and `rules`.
- Optional integrations (Pydantic, Beartype, PyUnitWizard).
- SMonitor-backed diagnostics.

---

## smonitor

ArgDigest emits structured diagnostics when digestion warnings occur. Configuration
is loaded from `_smonitor.py` in the package root (`argdigest/_smonitor.py`), and
the catalog lives in `argdigest/_private/smonitor/catalog.py` with metadata in
`argdigest/_private/smonitor/meta.py`.

## 📖 Documentation

Full documentation is available at [uibcdf.org/argdigest](https://uibcdf.org/argdigest).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
