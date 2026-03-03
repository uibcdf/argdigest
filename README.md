# ArgDigest

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/137937243.svg)](https://zenodo.org/badge/latestdoi/137937243)
[![](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/uibcdf/argdigest/actions/workflows/CI.yaml/badge.svg)](https://github.com/uibcdf/argdigest/actions/workflows/CI.yaml)
[![codecov](https://codecov.io/github/uibcdf/argdigest/graph/badge.svg?token=rkYkIOfPIs)](https://codecov.io/github/uibcdf/argdigest)
[![Install with conda](https://img.shields.io/badge/Install%20with-conda-brightgreen.svg)](https://conda.anaconda.org/uibcdf/argdigest)

*Digesting function arguments into clear, reliable contracts.*


## Overview

**ArgDigest** is a Python library for **digesting function arguments** at API boundaries.
It helps libraries normalize, validate, and standardize inputs with explicit,
reusable contracts.

It combines:
- **Argument-centric digestion** (per-argument digesters),
- **Pipeline rules** (reusable validation/coercion by kind and rule name),
- **Structured diagnostics** (clear warnings and errors with context).

## Installation

```bash
pip install argdigest
```

Optional integrations:

```bash
pip install argdigest[beartype]
pip install argdigest[pydantic]
pip install argdigest[pyunitwizard]
pip install argdigest[all]
```

## Quick example

```python
from argdigest import arg_digest

@arg_digest(
    config="mylib._argdigest",
    strictness="warn",
    map={"syntax": {"kind": "std", "rules": ["is_str"]}},
)
def get(molecular_system, selection=None, syntax="MolSysMT"):
    return molecular_system, selection, syntax
```

Typical style options:
- `package`: one module per argument (`digest_<argument>`),
- `registry`: central mapping (`ARGUMENT_DIGESTERS`),
- `decorator`: registration via `@argument_digest("arg")`,
- `auto`: mixed mode for incremental migrations.

## Diagnostics model (SMonitor)

ArgDigest emits catalog-based diagnostics through SMonitor.

Runtime/config files:
- `argdigest/_smonitor.py`
- `argdigest/_private/smonitor/catalog.py`
- `argdigest/_private/smonitor/meta.py`

## Documentation

- User + developer docs: [uibcdf.org/argdigest](https://uibcdf.org/argdigest)
- Internal roadmap and implementation notes: `devguide/`

## License

MIT. See [LICENSE](LICENSE).
