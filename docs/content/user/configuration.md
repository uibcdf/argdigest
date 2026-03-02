# Configuration

ArgDigest supports three configuration levels. Use them in this precedence order
(highest first):

1. Explicit decorator arguments (`digestion_source`, `digestion_style`, `strictness`, etc.).
2. Explicit configuration module (`config="mylib._argdigest"`).
3. Auto-discovered module (`<root_package>._argdigest`) when no explicit config is provided.

## Recommended `_argdigest.py` template

```python
# mylib/_argdigest.py

DIGESTION_SOURCE = "mylib._private.digestion.argument"
DIGESTION_STYLE = "package"  # package | registry | decorator | auto
STANDARDIZER = "mylib._private.digestion.normalization.standardizer:argument_names_standardization"
STRICTNESS = "warn"          # warn | error | ignore
SKIP_PARAM = "skip_digestion"
```

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
    digestion_source="mylib._private.digestion.argument",
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
