# Template: Registry-style digestion

Use this template when the library prefers a central registry rather than one file per argument.

## Goal
- Define a module exposing `ARGUMENT_DIGESTERS`.
- ArgDigest discovers digesters via `digestion_style="registry"`.

## Required structure
```
my_lib/
  _argdigest.py
  _private/
    argdigest/
      registry.py
```

## Library config (`my_lib/_argdigest.py`)
```python
DIGESTION_SOURCE = "my_lib._private.argdigest.registry"
DIGESTION_STYLE = "registry"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
FUNCTION_SOURCE = "my_lib._private.argdigest.function"
DOMAIN_SOURCE = "my_lib._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"
NORMALIZATION_SOURCE = "my_lib._private.argdigest.normalization"
```

## Programmatic config alternative (`my_lib/__init__.py`)
```python
import argdigest.config

argdigest.config.set_defaults(
    digestion_source="my_lib._private.argdigest.registry",
    digestion_style="registry"
)
```

## Registry module (`registry.py`)
```python
def digest_a(a, caller=None):
    return int(a)


def digest_b(b, a=None, caller=None):
    return int(b) + int(a)


ARGUMENT_DIGESTERS = {
    "a": digest_a,
    "b": digest_b,
}
```

## Usage in public API
```python
from argdigest import arg_digest

@arg_digest(config="my_lib._argdigest")
def analyze(a, b, skip_digestion=False):
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
