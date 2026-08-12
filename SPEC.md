---
title: ArgDigest Technical Specification
version: 0.2
authors: [UIBCDF Development Team]
license: MIT
---

# ArgDigest Technical Specification

## 1. Overview

**ArgDigest** is a lightweight and extensible library for **auditing, validating, and normalizing function arguments** in scientific and analytical Python libraries.

ArgDigest covers **two axes**, and a library needs both:

1. **The function's argument contract** — *may this function receive this argument at
   all, and does it have what it needs?* Declared as `FunctionContract` and `Domain`.
2. **The argument's value contract** — *given an argument name, is its value valid and
   in canonical form?* Declared as per-argument digesters.

Without axis 1, function-dependent rules have nowhere to live and end up scattered
across the per-argument digesters, one `if caller == ...` at a time, so the contract of
a function is never written down in one readable place. Axis 1 gives it a home.

Its purpose is to provide a generic infrastructure that:
- Verifies the **coherence and type** of input arguments.
- **Coerces** heterogeneous objects into the expected internal forms.
- Applies **domain-specific semantic rules** (e.g., topography, molecular systems).
- Produces **consistent and clear error messages** with context and hints.
- Enables **shared and reusable validation pipelines** across different projects (e.g., MolSysMT, TopoMT).

---

## 2. Architecture

The library is structured to separate core logic from domain implementations:

```
argdigest/
  core/
    decorator.py        # Main @arg_digest logic and orchestration
    registry.py         # Pipeline registry (kind/rules)
    argument_registry.py# Argument-centric registry (@argument_digest)
    argument_loader.py  # Discovery logic (packages, modules)
    function_contract.py# Axis 1: FunctionContract, Domain, resolution and checking
    normalization.py    # Declared argument-name aliases (AliasTable)
    function_loader.py  # Discovery of contracts, domains and alias tables
    context.py          # Execution context (function, argname, value)
    errors.py           # Rich exception hierarchy
    logger.py           # Centralized logging
    config.py           # Configuration resolution
    utils.py            # Helper functions (binding, etc.)
  pipelines/            # Built-in generic pipelines
  contrib/              # Integrations (beartype, pydantic)
tests/
docs/
```

---

## 3. Public API

### 3.1 The `@arg_digest` Decorator

The primary entry point is the `@arg_digest` decorator. It supports both **argument-centric discovery** (auto-finding how to digest an argument) and **explicit pipeline mapping**.

```python
@arg_digest(
    # Configuration for Argument-Centric Mode
    digestion_source=None,       # str | list[str]: Module/package paths to search
    digestion_style="auto",      # "auto" | "registry" | "package" | "decorator"
    standardizer=None,           # callable | "module:func": Normalizes arg names
    strictness="warn",           # "warn" | "error" | "ignore": For missing digesters
    skip_param="skip_digestion", # str: Name of param to bypass digestion
    
    # Configuration for Explicit Mode
    map=None,                    # dict: Explicit {arg: {kind, rules}} mapping
    kind=None,                   # str: Default kind for all args (if map is None)
    rules=None,                  # list[str]: Default rules for all args
    
    # Extra config
    config=None                  # str | object: Config object or module path
)
def my_func(...): ...
```

### 3.2 The `arg_digest.map` Alias

A convenient alias for defining explicit mappings using keyword arguments:

```python
arg_digest.map(
    arg_name={"kind": "feature", "rules": ["validate_shape"]},
    other_arg={"kind": "topology"}
)
def my_func(arg_name, other_arg): ...
```

### 3.3 Registration Decorators

- **`@argument_digest(arg_name)`**: Registers a function to digest a specific argument name globally (used in `digestion_style="decorator"`).
- **`@register_pipeline(kind, name)`**: Registers a reusable pipeline function (coercer/validator) for a specific semantic kind.

---

## 4. Digestion Logic & Behavior

### 4.1 Argument-Centric Discovery
When `digestion_source` or `digestion_style` is used, ArgDigest attempts to find a "digester" function for each argument.

**Discovery Styles:**
- **`registry`**: Looks for an `ARGUMENT_DIGESTERS` dictionary in the `digestion_source` module.
- **`package`**: Scans the `digestion_source` package for functions named `digest_<arg_name>`.
- **`decorator`**: Uses the global registry built by `@argument_digest`.
- **`auto`**: Tries `registry` → `package` → `decorator` in order, merging results.

**Behavior Contracts:**
1.  **Skip**: If `skip_param=True` is passed to the function, **all digestion is skipped**.
2.  **Execution**:
    - If a digester is found, it is executed. The digester receives the raw value and can request other arguments (dependency injection).
    - If no digester is found, `strictness` determines the action (`warn`, `error`, or `ignore`).
    - If no argument-centric configuration is provided and no digesters are discovered, ArgDigest runs in pipeline-only mode without emitting missing-digester warnings.
3.  **Result**: The original function is called with the *transformed* values.

### 4.2 Dependency Resolution
Digesters can declare dependencies on other arguments.
- ArgDigest resolves the execution order (topological sort).
- **Cycles**: If a cycle is detected (e.g., `a` needs `b`, `b` needs `a`), a `DigestNotDigestedError` is raised with the full cycle path (e.g., `a -> b -> a`).

### 4.3 Hooks
- **Standardizer**: Runs *before* digestion. It normalizes argument names (e.g., converting aliases like `sel` to `selection`) so that digesters match correctly.

### 4.4 Call shape

Digestion works on a flat `name -> value` mapping, which is what makes a digester
reachable by argument name. The wrapped function is then called back **in the shape it
was declared**, not as `fn(**mapping)`: a var-positional parameter has no keyword form
at all, and a positional-only one refuses to be named, so both would arrive wrong or not
arrive.

- `*args` is bound as a single tuple, digested once under the parameter's own name, and
  **unpacked** when the function is called. A digester named for the parameter therefore
  receives the whole collection, which is what lets it assert something about the group
  rather than about one operand.
- Positional-only parameters (`/`) are passed positionally.
- A non-empty `*args` forces the parameters before it to travel positionally too; when it
  is empty they stay keywords.

Which of the two call forms applies is a property of the signature, decided once at
decoration time, so a signature with neither feature keeps the single dict unpack.

---

## 5. Error Model

Exceptions are rich objects inheriting from `DigestError`. They include:
- `message`: Human-readable description.
- `context`: A `Context` or `SimpleNamespace` object containing:
    - `function_name`: Where the error occurred.
    - `argname`: The specific argument involved.
    - `value`: The runtime value (truncated representation).
- `hint`: Actionable advice for the user.

**Hierarchy:**
- `DigestError`
  - `DigestTypeError`: Type mismatch.
  - `DigestValueError`: Semantic validation failure.
  - `DigestInvariantError`: Multi-argument rule violation.
  - `DigestNotDigestedError`: Missing digester (when strictness="error") or cyclic dependency.
- `FunctionContractError`: Base for axis-1 breaches.
  - `UnknownArgumentError`: An argument the function does not accept.
  - `MissingArgumentError`: A call satisfying no required argument group.
  - `ArgumentConsistencyError`: Mutually exclusive or co-required arguments misused.

`FunctionContractWarning` reports the same breaches when `unknown_argument="warn"`.

---

## 6. Axis 1: The Function Argument Contract

### Why the default is strict

Plain Python raises `TypeError` for an unexpected keyword. **ArgDigest must never end up
more permissive than the language it wraps**, so `unknown_argument` defaults to
`"error"`. This is not a new policy: it restores parity, with a better diagnostic and a
near-miss suggestion.

### What a consumer declares

Only data. Discovery, resolution order, enforcement and introspection stay in ArgDigest.

```python
# mylib/_argdigest.py
FUNCTION_SOURCE = "mylib._private.argdigest.function"
DOMAIN_SOURCE = "mylib._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"          # "error" | "warn" | "ignore"
```

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

A module may declare one `contract`/`domain` or a list in `CONTRACTS`/`DOMAINS`.

### Defaults when nothing is declared

| Function | Default contract |
| --- | --- |
| closed signature | held to its own parameters |
| declares `**kwargs` | admits anything until a domain is declared |

A closed signature already declares its domain, so it is protected for free. A function
with `**kwargs` deliberately opened its door and ArgDigest cannot guess what it meant.

### Resolution order

Exact `caller`, then the **longest matching** `caller_pattern` (fnmatch), then the
default. Longest-pattern-wins keeps specificity predictable without asking consumers to
declare priorities, and lets a whole family of adapters share one contract.

### Where it runs

`bind_arguments` → **normalization** → standardizer → **contract** → digestion.

After the standardizer, so an alias that has just become its canonical name is never
mistaken for a typo. Before digestion, because validating the value of an argument that
should not be there is wasted work with a confusing failure. `bind_arguments` sets aside
the keywords a closed signature cannot take and hands them to this stage rather than
discarding them, so the policy layer sees what the caller actually wrote.

### Introspection

`describe_contract(contract, domains)` renders a contract as plain data. This is why a
contract is declarative rather than an opaque callable: the accepted domain of a
`**kwargs` function is invisible to `inspect.signature`, and this makes it readable
again — for documentation, IDEs and agents.

### A domain that depends on another argument

`Domain(depends_on=..., by_value=...)` declares the admissible set per value of another
argument, keyed by one name or by a tuple of names. It stays data, so `describe_contract`
renders the whole table. A value with no entry means "cannot decide", not "refuse": the
argument carrying it is about to be rejected by its own digester.

The key must be an argument, not a derivation. The table is consulted per call, so
deciding the domain has to be cheap.

### Known limit

`by_value` keys on **arguments**, read directly from the call. A domain whose key must be
*derived*, when the derivation is expensive, does not fit: consulting it per call would
cost more than the check saves. Group the key so it stays cheap, and accept the wider
union that follows, or leave the function permissive and record the measurement.

`by_value` accepts any `Mapping`, so a table with hundreds of entries can compute itself
lazily rather than being written out. A table derived from live signatures cannot go
stale, but it can silently shrink if one of those signatures becomes unreadable, so it
should be paired with a check that fails when that happens.

---

## 6b. Declared normalization

Argument-name aliases are declared as data in `NORMALIZATION_SOURCE`, one module per
family of rules exposing `table` or `TABLES`:

```python
from argdigest import AliasTable

AliasTable(aliases={'residue_index': 'group_index'})                    # global
AliasTable(applies_to='mylib.form.*', aliases={'idx': 'index'})        # family
AliasTable(applies_to='mylib.basic.get.get', when={'element': 'atom'}, # context
           aliases={'name': 'atom_name'})
```

`applies_to` is an exact caller, an `fnmatch` pattern or `"*"`. `when` is an equality test
against already-bound arguments, deliberately not an expression language.

Tables compose most-specific-first; renaming is one pass and never chains; argument order
is preserved. `describe_normalization` renders them as data.

Normalization runs **before** the function contract, which is what lets a library declare
contracts without breaking its aliases: by the time a keyword is judged it is canonical,
while a genuine typo survives unchanged and is refused.

The `standardizer` hook still runs, after the declared tables. Its contract,
`(caller, kwargs) -> mapping`, is now verified: the signature when the decorator is built
and the return value on every call, reported as `StandardizerContractError`.

## 7. Compatibility Profiles

### 7.1 MolSysMT Profile
Recommended configuration for MolSysMT integration:

MolSysMT configures both axes from one module, `molsysmt._argdigest`:

```python
DIGESTION_SOURCE = "molsysmt._private.argdigest.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"

FUNCTION_SOURCE = "molsysmt._private.argdigest.function"
DOMAIN_SOURCE = "molsysmt._private.argdigest.domain"
NORMALIZATION_SOURCE = "molsysmt._private.argdigest.normalization"
UNKNOWN_ARGUMENT = "error"
```

MolSysMT declares **no** `STANDARDIZER`: everything it used to rename by hand is now
declared as alias tables, which is what the hook is meant to make unnecessary.

`STRICTNESS` and `UNKNOWN_ARGUMENT` answer different questions and have different
audiences. A missing digester for a declared parameter is a to-do for the library
author, so `warn` is right. A keyword nobody declared is a mistake by whoever made the
call, and warning about it is not enough — warnings are routinely filtered off exactly
where users read output.

---

## 8. Examples

### Explicit Mapping
```python
from argdigest import arg_digest, register_pipeline

@register_pipeline(kind="feature", name="is_2d")
def check_2d(val, ctx):
    if val.dim != 2: raise ValueError("Not 2D")
    return val

arg_digest.map(
    surface={"kind": "feature", "rules": ["is_2d"]}
)
def calculate_area(surface):
    ...
```

### Argument-Centric (Package Style)
File: `mylib/_private/argdigest.py`
```python
def digest_volume(volume, caller=None):
    return float(volume)
```

File: `mylib/api.py`
```python
@arg_digest(digestion_source="mylib._private.argdigest", digestion_style="package")
def compute(volume):
    # volume is guaranteed to be float here
    ...
```
