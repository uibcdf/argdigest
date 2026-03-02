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
# mylib/_private/digestion/argument/selection.py
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
DIGESTION_SOURCE = "mylib._private.digestion.argument"
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

Run two quick checks: `get(..., selection=None)` should produce
`selection="all"`, and `get(..., selection=10)` should fail with a digestion
error. This confirms both normalization and failure behavior are wired.

## Common mistakes

Most first-time failures come from three causes: the digester function is not
named `digest_<argument>`, `digestion_source` points to the wrong module/package,
or strict behavior is assumed without configuring it explicitly.

## You are done when

- the decorated function runs with normalized arguments,
- invalid inputs fail with actionable errors,
- your library does not need custom digestion logic inside business functions.

## Next

Continue with [Mini Library Walkthrough](mini-library-walkthrough.md).
