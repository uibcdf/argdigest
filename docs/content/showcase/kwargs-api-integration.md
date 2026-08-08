# Integrating an API with `**kwargs`

Use this pattern when a function accepts a large, open set of keywords — attribute names,
property names, feature flags — that can never be signature parameters.

It is the one case where a library **must** declare something for the function argument
contract to work. Every closed signature is covered for free.

## The problem

```python
msm.get(molsys, n_atoms=True, coordinates=True)
```

There are 118 attribute names. Listing them as parameters is not an option, so the
function takes `**kwargs`. And a function taking `**kwargs` accepts *anything* — so
`n_atomss=True` is discarded in silence, the call runs with the default, and the caller
receives a well-formed, wrong answer.

## Structure

```text
mylib/
  _argdigest.py
  attribute.py                     # the library's own catalogue of valid names
  _private/argdigest/
    argument/                      # axis 2: one module per argument name
    domain/
      attribute.py                 # the set of admissible keywords
    function/
      get.py                       # which functions admit that set
```

## `_argdigest.py`

```python
DIGESTION_SOURCE = "mylib._private.argdigest.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"

FUNCTION_SOURCE = "mylib._private.argdigest.function"
DOMAIN_SOURCE = "mylib._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"
```

## The domain

```python
# mylib/_private/argdigest/domain/attribute.py
from argdigest import Domain

from mylib.attribute import attributes, is_attribute

domain = Domain(
    name='attribute',
    contains=is_attribute,
    members=lambda: tuple(attributes),
    description='canonical attribute names',
)
```

**Point at the catalogue; do not copy it.** A domain that reads the library's own source
of truth cannot drift away from it, and a domain that lists names by hand will.

`contains` decides membership and `members` enumerates it. The enumeration is what makes
near-miss suggestions and introspection possible, so provide it when the set is finite.

## The contract

```python
# mylib/_private/argdigest/function/get.py
from argdigest import FunctionContract

CONTRACTS = [
    FunctionContract(caller='mylib.basic.get.get', admits='attribute'),
    FunctionContract(caller='mylib.basic.set.set', admits='attribute'),
    FunctionContract(caller='mylib.basic.contains.contains', admits='attribute'),
]
```

Several functions usually share one domain. Declare the domain once and point each
function at it rather than repeating the set.

## What the caller sees

```
>>> mylib.get(system, n_atomss=True)
UnknownArgumentError: 'mylib.basic.get.get' does not accept the argument 'n_atomss'.
Did you mean 'n_atoms'?
```

## Requirements and exclusions

A contract can also state rules that would otherwise live inside the function body:

```python
FunctionContract(
    caller='mylib.structure.get_neighbors.get_neighbors',
    mutually_exclusive=[('threshold', 'n_neighbors')],
    requires_any_of=['threshold', 'n_neighbors'],
)
```

Moving such a rule out of the body makes it fail before any work is done, and upgrades a
bare `ValueError` into a catalogued diagnostic naming both arguments.

Be careful with what a rule actually means. `requires_any_of` and `co_required` test
**presence**; a rule conditional on a *value* — "if `pairs=True` then both flags must be
true" — is not the same thing and does not belong in a contract.

## When you cannot declare a domain

If the admissible keywords depend on something resolved at call time, such as a converter
chosen by another argument, a `Domain` cannot express it: membership is decided from the
keyword alone. Leave that function on the permissive default and record why, rather than
declaring a domain that is not the real one.

## Smoke check

1. A valid keyword from the domain passes untouched.
2. A near miss is refused and the message suggests the intended name.
3. A closed signature in the same library refuses an unknown keyword with no declaration.
4. `describe_contract` lists the domain, so the accepted names can be documented.
