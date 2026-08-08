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
STRICTNESS = "warn"          # warn | error | ignore
SKIP_PARAM = "skip_digestion"

# Axis 1 -- the argument contract of each function.
FUNCTION_SOURCE = "mylib._private.argdigest.function"
DOMAIN_SOURCE = "mylib._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"   # error | warn | ignore

# Declared argument-name aliases, applied before both axes.
NORMALIZATION_SOURCE = "mylib._private.argdigest.normalization"
```

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

## Practical guidance

- Prefer a single `_argdigest.py` per library package.
- Use explicit decorator overrides only for exceptional endpoints.
- Keep configuration values stable and documented for contributors.

## Next

Continue with [Configuration Precedence](config-precedence.md).
