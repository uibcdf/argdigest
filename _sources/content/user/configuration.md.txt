# Configuration

ArgDigest supports three configuration levels. Use them in this precedence order
(highest first):

1. Explicit decorator arguments (`digestion_source`, `digestion_style`, `strictness`, etc.).
2. Explicit configuration module (`config="mylib._argdigest"`).
3. Environment module (`ARGDIGEST_CONFIG="mylib._argdigest"`).
4. Auto-discovered module (`<root_package>._argdigest`) when no explicit config is provided.

## Recommended `_argdigest.py` template

```python
# mylib/_argdigest.py

# Axis 2 -- the value contract of each argument.
DIGESTION_SOURCE = "mylib._private.argdigest.argument"
DIGESTION_STYLE = "package"  # package | registry | decorator | auto
STANDARDIZER = "mylib._private.argdigest.argument_names_standardization:argument_names_standardization"
STRICTNESS = "warn"  # warn | error | ignore
ARGUMENT_DIGESTION = None  # None infers | True enables | False selects pipelines only
SKIP_PARAM = "skip_digestion"

# Axis 1 -- the argument contract of each function.
FUNCTION_SOURCE = "mylib._private.argdigest.function"
DOMAIN_SOURCE = "mylib._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"  # error | warn | ignore

# Declared argument-name aliases, applied before both axes.
NORMALIZATION_SOURCE = "mylib._private.argdigest.normalization"

# Diagnostics only; requires SMonitor's public scoped-capture capability.
CAPTURE_POLICY = None  # inherit | "metadata_only" | "detailed" | CapturePolicy
```

## Contract ownership under inheritance

Since ArgDigest 0.17.0, `DigestConfig.contract_owner`
separates contract lookup from diagnostic display. Its default, `None`, preserves
existing caller resolution exactly, including instance dispatch in classes
assembled from mixins.

Use `"definition"` when inherited methods should keep the contracts of their
implementation:

```python
from argdigest import DigestConfig, arg_digest

inherited_contracts = DigestConfig(contract_owner="definition")


class Base:
    @arg_digest(config=inherited_contracts)
    def process(self, value):
        return value


class Child(Base):
    pass
```

The selected key follows the existing `module.function` convention: here it is
the defining module plus `.process`, without a class component. Each function
resolves its own key when decorated, so the same configuration can be shared
with other methods. A separately decorated override resolves its own definition.
This mode uses function metadata and does not import an owner module.
Classes defining the same method name in one module share this existing key
convention; use distinct exact keys if their contracts must be disambiguated.

For a logical owner different from the implementation, provide an exact key,
for example `DigestConfig(contract_owner="mylib.native.model.__init__")`.
An exact key applies literally to every function using that configuration;
use a dedicated configuration when it belongs to one method. Keys consist of
two or more dotted Python identifiers. Patterns, blank keys and malformed keys
are rejected when the configuration is constructed. A valid key need not name
an importable function or an existing declaration; ordinary contract fallback
and matching rules still apply.

The selected key is shared by alias normalization, standardizers,
function/domain contract lookup and digester `caller`. For bound instance and
class methods, digester `qualname` retains the runtime class. Static methods
and free functions retain their defining qualified name because no receiver
identifies a runtime class. Function-contract refusals use that same display
identity when explicit ownership is active. Signature binding, value validation,
unknown-argument refusal and explicit digestion selection remain active.

Both decorator forms accept it through `config=DigestConfig(...)`. Python
configuration modules/files use `CONTRACT_OWNER`; JSON/YAML use
`contract_owner`. Existing arbitrary decorator context named `contract_owner`
keeps its original meaning: `arg_digest(contract_owner=...)` alone does not
select this policy. Wrapped-function call arguments cannot change the policy.

Inspect `function.digestion_plan.contract_owner` for the requested selection and
`function.digestion_plan.contract_caller` for the resolved fixed key (`None`
means runtime resolution). The CLI audit reports both fields.

## Strictness and unknown arguments

Both policies accept the same aliases: `raise` -> `error`, `warning` -> `warn`,
`silent`/`none` -> `ignore`.

### The two policies are not the same knob

| | Fires when | Who made the mistake | Default |
| --- | --- | --- | --- |
| `STRICTNESS` | a declared parameter has no digester | the library author | `warn` |
| `UNKNOWN_ARGUMENT` | a keyword is outside the function's contract | whoever made the call | `error` |

A missing digester is a to-do for you, so a warning is right. A keyword nobody declared
is a caller's typo, and warning is not enough: warnings are routinely filtered off
exactly where users read output, and the call would then run with the default and return
a plausible wrong answer.

`FUNCTION_SOURCE` and `DOMAIN_SOURCE` are optional. Without them every closed signature
is still held to its own parameters -- ArgDigest never ends up more permissive than
Python -- and only functions taking `**kwargs` stay unconstrained until you declare the
domain their keywords come from.

## Using config in decorators

```python
from argdigest import arg_digest

@arg_digest(config="mylib._argdigest")
def get(...):
    ...
```

## Programmatic defaults (optional)

You can set defaults programmatically at import time:

```python
import argdigest.config

argdigest.config.set_defaults(
    digestion_source="mylib._private.argdigest.argument",
    digestion_style="package",
    strictness="warn",
)
```

## Select argument digestion explicitly

Providing configuration participates in the historical automatic selection of
argument digesters. For a boundary that only uses pipelines, select
`argument_digestion=False` explicitly:

```python
from argdigest import DigestConfig, arg_digest

cfg = DigestConfig(strictness="error", argument_digestion=False)


@arg_digest.map(config=cfg, name={"kind": "std", "rules": ["strip", "upper"]})
def normalize_name(name):
    return name


assert normalize_name(" name ") == "NAME"
```

| Selection | Argument digesters | Missing-digester policy |
| --- | --- | --- |
| `None` (default) | Historical inference from configuration and discovered digesters | Applies when inferred active |
| `True` | Discover and execute selected digesters | Uses `strictness` |
| `False` | Do not discover or execute argument digesters | Inactive |

`False` keeps Python binding, declared function/domain contracts, alias
normalization, the standardizer, pipelines and requested type checks active.
It differs from `skip_digestion=True`, which bypasses processing for a call.
`digestion_style` chooses a discovery source; it does not select execution.

Use the same selector on `arg_digest`, `arg_digest.map` or `DigestConfig`.
Python modules/files use `ARGUMENT_DIGESTION`; JSON/YAML files use
`argument_digestion` with a boolean or null. Explicit decorator selection takes
precedence, including an explicit `None` to restore automatic inference.
The callable's `digestion_plan.argument_digestion` records the requested selector;
`digestion_plan.enable_argument_digestion` records the effective boolean.
`argdigest audit` displays both.

## Practical guidance

- Prefer a single `_argdigest.py` per library package.
- Use explicit decorator overrides only for exceptional endpoints.
- Keep configuration values stable and documented for contributors.

## Next

Continue with [Configuration Precedence](config-precedence.md).

`DigestConfig(capture_policy=...)` and Python configuration modules use the same
policy selection as the decorator. JSON/YAML files use `capture_policy` with a
named string. See [scoped diagnostic capture](smonitor.md#restrict-collection-before-validation)
for availability, compatibility and concurrency boundaries.
