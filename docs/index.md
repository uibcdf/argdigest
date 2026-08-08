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

## Two axes

That example covers one half of the problem: *given an argument name, is its value valid
and in canonical form?* A library also needs the other half: *may this function receive
this argument at all, and does it have what it needs?*

| Axis | You declare |
| --- | --- |
| **The function argument contract** | a `FunctionContract` per function or family, and a `Domain` for functions taking `**kwargs` |
| **The argument value contract** | one digester per argument name |

Without the first, a mistyped keyword is silently discarded, the call runs with the
default, and you get back a plausible wrong answer. ArgDigest refuses it instead:

```
UnknownArgumentError: 'mylib.basic.get.get' does not accept the argument 'n_atomss'.
Did you mean 'n_atoms'?
```

A **closed signature needs no declaration**: it is held to its own parameters, because
ArgDigest must never end up more permissive than Python, which already raises
`TypeError` for an unexpected keyword. A function taking `**kwargs` opened its door on
purpose, so it declares the domain those keywords come from:

```python
# mylib/_private/argdigest/domain/attribute.py
from argdigest import Domain
from mylib.attribute import attributes, is_attribute

domain = Domain(name='attribute', contains=is_attribute,
                members=lambda: tuple(attributes))
```

```python
# mylib/_private/argdigest/function/get.py
from argdigest import FunctionContract

contract = FunctionContract(caller='mylib.basic.get.get', admits='attribute')
```

Pointing the domain at your library's own catalogue, rather than copying names into a
list, is what keeps the two from drifting apart. `describe_contract` then renders the
whole thing as data, which is how the real domain of a `**kwargs` function becomes
readable — something `inspect.signature` cannot show.

:::{note}
`unknown_argument` defaults to `error` from version `0.10.0`. Set
`UNKNOWN_ARGUMENT = "warn"` or `"ignore"` in your configuration module during a
migration.
:::


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
