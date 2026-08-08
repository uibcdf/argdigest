# Integrating Your Library

Use this page as a migration blueprint for existing codebases.

## Minimum viable integration (one afternoon)

If time is limited, focus on one tight slice: add `_argdigest.py`, migrate one
high-traffic API function, implement digesters for the two or three arguments
that create most support friction, declare a contract for it if it takes `**kwargs`,
and add tests for valid, invalid, and bypass paths. This usually gives immediate consistency improvements without a large
migration.

## First principle

Treat ArgDigest adoption as an API-boundary refactor:
- move digestion logic out of business code,
- make behavior explicit and testable,
- keep one contract source for contributors.

## The integration has two halves

An integration that declares only argument digesters is half an integration.

| Axis | Question it answers | What you write |
| --- | --- | --- |
| **1. The function argument contract** | may this function receive this argument at all, and does it have what it needs? | a `FunctionContract` per function or family, and a `Domain` for the keywords a `**kwargs` function accepts |
| **2. The argument value contract** | is this argument's value valid and in canonical form? | one digester per argument name |

The good news is that half of axis 1 costs nothing. **A closed signature is already a
domain**, so it is held to its own parameters the moment you decorate it, with no
declaration at all — ArgDigest never ends up more permissive than Python, which already
raises `TypeError` for an unexpected keyword.

What needs declaring is the other case: a function taking `**kwargs` opened its door on
purpose, and ArgDigest cannot guess what it meant. Until you declare its domain, that
function accepts anything — and a mistyped keyword is silently discarded, the call runs
with the default, and the caller gets back a plausible wrong answer.

## Phase 1: establish configuration

1. Add `mylib/_argdigest.py`.
2. Choose one digestion style (`package`, `registry`, or `decorator`).
3. Configure `strictness="warn"` for initial rollout.
4. Point `FUNCTION_SOURCE` and `DOMAIN_SOURCE` at the packages where you will declare
   contracts and domains. They may start empty.

Checkpoint:
- the package imports cleanly,
- one decorated function runs with digesters active.

## Phase 2: migrate high-value functions

Start with:
- public API entry points,
- functions that currently have repeated argument checks,
- functions with known user confusion around argument semantics.

Checkpoint:
- digestion logic is removed from function bodies in migrated modules.

## Phase 3: declare what each function accepts

Every function taking `**kwargs` needs the domain of those keywords declared. Point the
domain at your library's own source of truth rather than copying names into a list, so
the two cannot drift apart:

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

This is also where a rule already living inside a function body belongs. Grep your code
for `raise ValueError` mentioning "at least one", "only one of", or "both": each is an
inter-argument rule that can move into a contract as `requires_any_of`,
`mutually_exclusive` or `co_required`, and moving it upgrades a bare exception into a
catalogued diagnostic for free.

Use `caller_pattern` for a family of adapters that share a contract; resolution is
most-specific-first, so an exact caller wins over the longest matching pattern.

Checkpoint:
- no function with `**kwargs` is left admitting anything,
- inter-argument rules live in contracts rather than in function bodies.

## Phase 4: add normalization and pipelines

1. Add a standardizer if argument aliases exist.
2. Register reusable pipelines for repeated validations.
3. Keep semantic checks close to digestion contracts.

Checkpoint:
- alias handling is consistent across functions,
- repeated validation code is replaced by pipeline rules.

## Phase 5: harden behavior

1. Add tests for invalid and edge inputs.
2. Track missing-digester warnings.
3. Move to `strictness="error"` when ready.

`UNKNOWN_ARGUMENT` is a separate decision and already defaults to `error`. If an existing
codebase relies on extra keywords being tolerated, set it to `warn` for the migration and
tighten it once the call sites are clean — but do not leave it there: a warning about a
typo is filtered off exactly where users read output.

Checkpoint:
- missing digesters are treated as integration defects,
- API behavior is stable and documented.

## Practical migration order

1. one module,
2. one argument family,
3. one subsystem at a time,
4. then global rollout.

## Expected gains during migration

As migration progresses, you should see less duplicated validation code in
business modules, more consistent behavior across similar entry points, and a
clearer support/debug path for invalid inputs.

## End-user communication

Even if end users do not know ArgDigest, they will see its effects through
validation messages. Include a short section in your host-library docs that
explains how to read these messages and how to report mismatches effectively.

## Next

Continue with [Examples](examples.md).
