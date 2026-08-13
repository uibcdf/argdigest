# Mini Library Walkthrough

This walkthrough shows a complete, small integration using package-style digesters
and library-level defaults in `_argdigest.py`, covering **both axes**: what each function
accepts, and what each argument's value must be.

## Project layout

```text
mylib/
  __init__.py
  _argdigest.py
  basic.py
  _private/
    digestion/
      argument/
        __init__.py
        selection.py
        syntax.py
```

## 1. Define library defaults

```python
# mylib/_argdigest.py
DIGESTION_SOURCE = "mylib._private.argdigest.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

## 2. Define digesters

```python
# mylib/_private/argdigest/argument/selection.py
def digest_selection(selection, syntax="MolSysMT", caller=None):
    if selection is None:
        return "all"
    if isinstance(selection, str):
        return selection
    if syntax == "MolSysMT" and isinstance(selection, int):
        return [selection]
    raise ValueError(f"Invalid selection in {caller}: {selection!r}")
```

```python
# mylib/_private/argdigest/argument/syntax.py
def digest_syntax(syntax, caller=None):
    if syntax is None:
        return "MolSysMT"
    if isinstance(syntax, str):
        return syntax
    raise ValueError(f"Invalid syntax in {caller}: {syntax!r}")
```

## 3. Decorate API functions

```python
# mylib/basic.py
from argdigest import arg_digest

@arg_digest(config="mylib._argdigest")
def get(molecular_system, selection=None, syntax=None, skip_digestion=False):
    return molecular_system, selection, syntax
```

## 4. Declare what each function accepts

`get` above has a closed signature, so it is already held to its own parameters: calling
it with `selectionn="all"` raises `UnknownArgumentError` suggesting `selection`, and you
declared nothing to get that.

A function taking `**kwargs` is the case that needs declaring, because ArgDigest cannot
guess what it meant:

```python
# mylib/_private/argdigest/domain/attribute.py
from argdigest import Domain

ATTRIBUTES = ("n_atoms", "n_bonds", "coordinates")

domain = Domain(name="attribute", contains=lambda k: k in ATTRIBUTES,
                members=lambda: ATTRIBUTES)
```

```python
# mylib/_private/argdigest/function/get_attributes.py
from argdigest import FunctionContract

contract = FunctionContract(
    caller="mylib.basic.get_attributes",
    admits="attribute",
    requires_any_of="attribute",   # asking for nothing would be meaningless
)
```

Then add to `_argdigest.py`:

```python
FUNCTION_SOURCE = "mylib._private.argdigest.function"
DOMAIN_SOURCE = "mylib._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"
```

In a real library the domain should point at whatever already defines those names, rather
than repeating them, so the two cannot drift apart.

## 5. Add one pipeline rule (optional)

```python
from argdigest import register_pipeline

@register_pipeline(kind="selection", name="selection.non_empty")
def selection_non_empty(value, ctx):
    if value == "":
        raise ValueError("selection cannot be empty")
    return value
```

Then attach it in `@arg_digest(map={...})` where needed.

## Expected result

- `selection` and `syntax` are digested before function logic executes.
- The integration remains localized in digestion modules, not spread across API code.
- Additional rules can be layered via pipelines without changing digesters.

## Next

Continue with [Configuration](configuration.md).
