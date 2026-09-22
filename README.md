# ArgDigest

[![MolSysSuite: Support Library](https://img.shields.io/badge/MolSysSuite-support%20library-2563eb?labelColor=24292f)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#support-library)
[![MolSysSuite policy](https://github.com/uibcdf/argdigest/actions/workflows/molsyssuite-policy.yml/badge.svg?branch=main)](https://github.com/uibcdf/argdigest/actions/workflows/molsyssuite-policy.yml)
[![Python 3.11 | 3.12 | 3.13 | 3.14](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md)
[![License](https://img.shields.io/github/license/uibcdf/argdigest)](https://github.com/uibcdf/argdigest/blob/main/LICENSE)
[![Tests](https://github.com/uibcdf/argdigest/actions/workflows/CI.yaml/badge.svg?branch=main)](https://github.com/uibcdf/argdigest/actions/workflows/CI.yaml)
[![Codecov](https://codecov.io/github/uibcdf/argdigest/graph/badge.svg)](https://codecov.io/github/uibcdf/argdigest)
[![Documentation](https://github.com/uibcdf/argdigest/actions/workflows/sphinx_docs_to_gh_pages.yaml/badge.svg)](https://www.uibcdf.org/argdigest/)
[![GitHub release](https://img.shields.io/github/v/release/uibcdf/argdigest)](https://github.com/uibcdf/argdigest/releases/latest)
[![Conda](https://img.shields.io/conda/vn/uibcdf/argdigest)](https://anaconda.org/uibcdf/argdigest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22892325.svg)](https://doi.org/10.5281/zenodo.22892325)

*Digesting function arguments into clear, reliable contracts.*


## Overview

**ArgDigest** is a Python library for **digesting function arguments** at API boundaries.
It helps libraries normalize, validate, and standardize inputs with explicit,
reusable contracts.

ArgDigest covers **two axes**, and a library needs both:

| Axis | Question | You declare |
| --- | --- | --- |
| **The function argument contract** | *May this function receive this argument at all, and does it have what it needs?* | a `FunctionContract`, and a `Domain` for functions taking `**kwargs` |
| **The argument value contract** | *Given an argument name, is its value valid and in canonical form?* | one digester per argument name |

It combines:
- **Function contracts** (what each function admits and requires),
- **Argument-centric digestion** (per-argument digesters),
- **Pipeline rules** (reusable validation/coercion by kind and rule name),
- **Structured diagnostics** (clear warnings and errors with context).

## Installation

ArgDigest is released on the `uibcdf` conda channel:

```bash
conda install -c uibcdf -c conda-forge argdigest
```

Both channels are needed: `depdigest` and `smonitor` come from `uibcdf`, the rest from
`conda-forge`.

There is no PyPI release yet, so `pip install argdigest` does not work. To work from
source:

```bash
git clone https://github.com/uibcdf/argdigest
cd argdigest
pip install -e .
```

### Optional integrations

The conda package carries the runtime dependencies only, so the integrations are
installed alongside it:

```bash
conda install -c uibcdf pyunitwizard
conda install -c conda-forge beartype pydantic
```

From a source checkout the same integrations are declared as extras:

```bash
pip install -e ".[beartype]"
pip install -e ".[pydantic]"
pip install -e ".[pyunitwizard]"
pip install -e ".[all]"
```

ArgDigest core supports Python 3.14. The optional PyUnitWizard integration remains
subject to PyUnitWizard's separate Python 3.14 transition; do not assume that extra
is available in a 3.14 environment yet.

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

### Declaring what a function accepts

A closed signature is held to its own parameters with no declaration at all: ArgDigest
never ends up more permissive than Python, which already raises `TypeError` for an
unexpected keyword.

A function taking `**kwargs` opened its door deliberately, so it declares the domain
those keywords come from — pointing at your library's own source of truth rather than
copying names:

```python
# mylib/_private/argdigest/domain/attribute.py
from argdigest import Domain
from mylib.attribute import attributes, is_attribute

domain = Domain(
    name="attribute", contains=is_attribute, members=lambda: tuple(attributes)
)
```

```python
# mylib/_private/argdigest/function/get.py
from argdigest import FunctionContract

contract = FunctionContract(caller="mylib.basic.get.get", admits="attribute")
```

Then a typo fails where it happens, instead of running with the default and returning a
plausible wrong answer:

```
UnknownArgumentError: 'mylib.basic.get.get' does not accept the argument 'n_atomss'.
Did you mean 'n_atoms'?
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
- Compatibility matrix: `docs/content/developer/compatibility-matrix.md`
- Internal roadmap and implementation notes: `devguide/`

## Current release status

- Current public tag: `0.13.0`, supporting Python 3.11--3.14.
- The `uibcdf` channel serves one `noarch` Conda artifact for all supported
  platforms and interpreters. The previous 0.12.1 line supported 3.11--3.13.
- The DOI badge identifies the project. Zenodo version DOI
  `10.5281/zenodo.22892326` archives the 0.13.0 source snapshot, not the
  Conda package.
- `1.0.0` tagging is intentionally gated by explicit release-owner confirmation.
- Go/no-go evidence pack: `devguide/1.0.0_go_no_go_pack.md`.

## License

MIT. See [LICENSE](LICENSE).
