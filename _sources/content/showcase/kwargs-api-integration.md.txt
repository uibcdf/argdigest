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

### A domain that depends on another argument

Sometimes which keywords are admissible depends on a value in the same call: an engine, an
output type, a mode. Declare the table and the argument it keys on:

```python
Domain(
    name='engine_options',
    depends_on='engine',
    by_value={
        'MolSysMT': ('threshold', 'parallel'),
        'OpenMM':   ('threshold', 'platform'),
    },
)
```

`depends_on` may name several arguments, in which case the table is keyed by a tuple.

It is still data: `describe_contract` renders the whole table, so the options each value
accepts can be documented rather than discovered by reading code.

**A value with no entry does not refuse anything.** It means the domain cannot decide for
this call — usually because that value is itself wrong — and the argument carrying it is
about to be rejected by its own digester, which explains the real problem far better than
a complaint about an unknown argument would.

**Key on an argument, not on a derivation.** The table is consulted per call, so the value
must be cheap to read. If deciding the domain requires computing something expensive from
another argument, the mechanism costs more than it saves and the function is better left
permissive with the reason recorded.

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

## A large table that computes itself

`by_value` takes any **Mapping**, and a mapping can be lazy. That is what makes the
mechanism usable for a dispatcher with hundreds of edges, where a hand-written table would
rot on the first signature change.

The live example is a converter dispatcher with 89 target forms and 561 edges, 80 of them
declared as module names so they are not imported until used. Its table knows its keys
without importing anything, and computes a value the first time that target is asked for:

```python
class ConverterArguments(Mapping):
    def __getitem__(self, to_form):
        if to_form not in self._cache:
            self._cache[to_form] = self._union_of_converter_signatures(to_form)
        return self._cache[to_form]
```

Measured: 2 µs per call once warm, and the lazy import happens on the first conversion to
that form — which is when it was going to happen anyway.

**Group the key so it stays cheap.** The exact set for that dispatcher depends on the pair
`(origin, target)`, but the origin is not an argument: deriving it costs 235 µs, about 14%
of a whole conversion, on every call. Keying on the target alone admits the union across
origins — measured, 4.9 names where the exact set averages 3.3. That is the right trade:
the comparison is not 4.9 against 3.3 but 4.9 against *anything*, a mistyped keyword
belongs to no union, and a keyword valid for another origin is rejected a moment later by
the converter, where the origin is known.

**Audit what computes itself.** A table derived from signatures cannot go stale, but it
can silently *shrink*: if a signature becomes unreadable the edge is skipped, its names
leave the domain, and valid calls start being refused. Keep a devtools check that fails
when that happens, and have it ask the domain rather than reimplement it.

## Smoke check

1. A valid keyword from the domain passes untouched.
2. A near miss is refused and the message suggests the intended name.
3. A closed signature in the same library refuses an unknown keyword with no declaration.
4. `describe_contract` lists the domain, so the accepted names can be documented.
