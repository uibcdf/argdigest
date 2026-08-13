# Template: Mixed style (package + pipelines)

Use this template when the library wants argument digesters **and** pipeline rules.

## Goal
- Argument digesters discovered from a package.
- Pipelines registered by `kind` and referenced in `@arg_digest(map=...)`.

## Required structure
```
my_lib/
  _argdigest.py
  _private/
    argdigest/
      argument/
        __init__.py
        selection.py
      function/
        __init__.py
        get.py
      domain/
        __init__.py
        attribute.py
      normalization/
        __init__.py
        synonyms.py
  pipelines/
    __init__.py
    base.py
```

## Library config (`my_lib/_argdigest.py`)
```python
DIGESTION_SOURCE = "my_lib._private.argdigest.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
FUNCTION_SOURCE = "my_lib._private.argdigest.function"
DOMAIN_SOURCE = "my_lib._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"
NORMALIZATION_SOURCE = "my_lib._private.argdigest.normalization"
```

## Pipeline example (`pipelines/base.py`)
```python
from argdigest import register_pipeline

@register_pipeline(kind="feature", name="feature.base")
def feature_base(obj, ctx):
    if not hasattr(obj, "feature_id"):
        raise ValueError("Missing feature_id")
    return obj
```

## Usage in public API
```python
from argdigest import arg_digest
from pydantic import BaseModel

class User(BaseModel):
    name: str

arg_digest.map(
    type_check=True, # Enforce beartype
    feature={"kind": "feature", "rules": ["feature.base"]},
    user={"kind": "data", "rules": [User]} # Native pydantic rule
)
def register_feature(feature, user, skip_digestion=False):
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
