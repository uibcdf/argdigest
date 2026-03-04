```{eval-rst}
:html_theme.sidebar_secondary.remove:
```

% ArgDigest

:::{figure} _static/logo.svg
:width: 50%
:align: center

Digesting function arguments into clear, reliable contracts.

```{image} https://img.shields.io/github/v/release/uibcdf/argdigest?color=white&label=release
:target: https://github.com/uibcdf/argdigest/releases
```
```{image} https://img.shields.io/badge/license-MIT-white.svg
:target: https://github.com/uibcdf/argdigest/blob/main/LICENSE
```
```{image} https://img.shields.io/badge/install%20with-conda-white.svg
:target: https://anaconda.org/uibcdf/argdigest
```
```{image} https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-white.svg
:target: https://www.python.org/downloads/
```
```{image} https://img.shields.io/badge/DOI-10.5281/8092688-white.svg
:target: https://zenodo.org/record/8092688
```

:::

<br>

## Install it

```bash
conda install -c uibcdf argdigest
```

## Use it

ArgDigest helps you normalize and validate input arguments at your API boundary,
without forcing a single internal architecture.

```python
from argdigest import arg_digest

@arg_digest(
    digestion_source="mylib._private.digestion.argument",
    digestion_style="package",
    strictness="warn",
)
def get(molecular_system, selection="all", syntax="MolSysMT"):
    return molecular_system, selection, syntax
```

What happens here:
- ArgDigest resolves digesters for each argument and applies them before your logic runs.
- If an argument cannot be digested, behavior follows your `strictness` policy.
- Optional diagnostics can be emitted through [SMonitor](https://www.uibcdf.org/smonitor).


```{eval-rst}

.. toctree::
   :maxdepth: 2
   :hidden:

   content/about/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   content/showcase/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   content/user/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   content/developer/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   api/index.md

```
