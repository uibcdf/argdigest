# Template: Package-style digestion

Use this template when the library will store one digester per argument under a package.

## Goal
- Each argument has a file `digest_<argument>` in `_private/argdigest/argument/`.
- ArgDigest discovers digesters via `digestion_style="package"`.

## Required structure
```
my_lib/
  _argdigest.py
  _private/
    argdigest/
      argument/
        __init__.py
        selection.py
        atom_index.py
      function/
        __init__.py
        get.py
      domain/
        __init__.py
        attribute.py
      normalization/
        __init__.py
        synonyms.py
      normalization/
        __init__.py
        standardizer.py
```

## Library config (`my_lib/_argdigest.py`)
```python
DIGESTION_SOURCE = "my_lib._private.argdigest.argument"
DIGESTION_STYLE = "package"
STANDARDIZER = "my_lib._private.argdigest.normalization.standardizer:standardizer"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
FUNCTION_SOURCE = "my_lib._private.argdigest.function"
DOMAIN_SOURCE = "my_lib._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"
NORMALIZATION_SOURCE = "my_lib._private.argdigest.normalization"
PUW_CONTEXT = {"standard_units": ["nm", "ps"]} # Optional: for Science libraries
```

## Programmatic config alternative (`my_lib/__init__.py`)
```python
import argdigest.config

argdigest.config.set_defaults(
    digestion_source="my_lib._private.argdigest.argument",
    digestion_style="package",
    strictness="warn"
)
```

## Digester template (`selection.py`)
```python
def digest_selection(selection, syntax="MyLib", caller=None):
    # Use standard pipelines internally if needed
    # from argdigest.pipelines.coercers import to_list
    # selection = to_list(selection)
    
    if selection is None:
        return "all"
    ...
```

## Usage in public API
```python
from argdigest import arg_digest

@arg_digest(config="my_lib._argdigest")
def get(molecular_system, selection=None, syntax="MyLib", skip_digestion=False):
    ...
```

## Declaring the function argument contract

Digesters cover one axis: *is this argument's value valid?* They cannot answer *may this
function receive this argument at all?* Without that second declaration a mistyped
keyword is silently discarded, the call runs with the default, and the caller gets back a
plausible wrong answer.

A **closed signature needs nothing**: ArgDigest holds it to its own parameters, because it
must never end up more permissive than Python, which already raises `TypeError` for an
unexpected keyword.

A function taking `**kwargs` must declare the domain of those keywords:

```python
# my_lib/_private/argdigest/domain/attribute.py
from argdigest import Domain
from my_lib.attribute import attributes, is_attribute

domain = Domain(name="attribute", contains=is_attribute,
                members=lambda: tuple(attributes))
```

```python
# my_lib/_private/argdigest/function/get.py
from argdigest import FunctionContract

contract = FunctionContract(caller="my_lib.basic.get.get", admits="attribute")
```

Point the domain at the library's own source of truth rather than copying names, so the
two cannot drift apart. A contract may also declare `requires_any_of`,
`mutually_exclusive` and `co_required`, and `caller_pattern` covers a family of functions
that share one contract.

## Declaring argument-name aliases

If the library should accept alternative names, declare them as data rather than renaming
by hand:

```python
# my_lib/_private/argdigest/normalization/synonyms.py
from argdigest import AliasTable

table = AliasTable(aliases={"residue_index": "group_index"})
```

Scope with `applies_to` when the alias only holds for one function or family, and guard
with `when={"element": "atom"}` when it depends on another argument of the same call.
Aliases are applied before the function contract, so declaring a contract never breaks
them.

## Notes
- If `@arg_digest()` is used without `config`, ArgDigest auto-detects `my_lib._argdigest`.
- Digesters can depend on other arguments (e.g., `syntax`) and ArgDigest resolves them.
