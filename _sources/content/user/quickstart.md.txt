# Quick Start

This is the fastest way to get a real ArgDigest integration.

## Goal

On this page, you create a minimal but real integration. The objective is to
reach a working setup with only three files: `mylib/_argdigest.py`, one digester
module, and one decorated API function. Once this works, expanding to more
arguments and modules is mostly repetition.

## 1. Install

```bash
conda install -c uibcdf argdigest
```

or from source:

```bash
python -m pip install --no-deps --editable .
```

## 2. Add a minimal digester

Create a digester module in your library:

```python
# mylib/_private/argdigest/argument/selection.py
def digest_selection(selection, caller=None, syntax=None):
    if selection is None:
        return "all"
    if isinstance(selection, str):
        return selection
    raise ValueError(f"Invalid selection in {caller}: {selection!r}")
```

## 3. Add `_argdigest.py`

```python
# mylib/_argdigest.py
DIGESTION_SOURCE = "mylib._private.argdigest.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

## 4. Decorate one function

```python
from argdigest import arg_digest

@arg_digest(
    config="mylib._argdigest",
    map={"syntax": {"kind": "std", "rules": ["is_str"]}},
)
def get(molecular_system, selection=None, syntax="MolSysMT"):
    return molecular_system, selection, syntax
```

## 5. Validate behavior

Run three quick checks:

- `get(..., selection=None)` produces `selection="all"` — normalization works;
- `get(..., selection=10)` fails with a digestion error — the value contract works;
- `get(..., selectionn="all")` fails with `UnknownArgumentError`, suggesting `selection`
  — the **function** contract works, and it needed no declaration at all.

That third check is the one people do not expect. `get` has a closed signature, so
ArgDigest holds it to its own parameters automatically: a mistyped keyword is refused
instead of being silently discarded and the call running with the default.

## 6. Declare a domain, if a function takes `**kwargs`

A function with `**kwargs` opened its door on purpose, and ArgDigest cannot guess what it
meant, so it admits anything until you say otherwise:

```python
# mylib/_private/argdigest/domain/attribute.py
from argdigest import Domain
from mylib.attribute import attributes, is_attribute

domain = Domain(name="attribute", contains=is_attribute,
                members=lambda: tuple(attributes))
```

```python
# mylib/_private/argdigest/function/get.py
from argdigest import FunctionContract

contract = FunctionContract(caller="mylib.basic.get.get", admits="attribute")
```

Then add `FUNCTION_SOURCE`, `DOMAIN_SOURCE` and `UNKNOWN_ARGUMENT` to `_argdigest.py`.
Pointing the domain at your library's own catalogue, rather than copying names into a
list, is what keeps the two from drifting apart.

## Common mistakes

Most first-time failures come from three causes: the digester function is not
named `digest_<argument>`, `digestion_source` points to the wrong module/package,
or strict behavior is assumed without configuring it explicitly.

## You are done when

- the decorated function runs with normalized arguments,
- invalid inputs fail with actionable errors,
- a mistyped keyword is refused rather than ignored,
- your library does not need custom digestion logic inside business functions.

## Next

Continue with [Mini Library Walkthrough](mini-library-walkthrough.md).
