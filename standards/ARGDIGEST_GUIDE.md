# ArgDigest Guide (Canonical)

Source of truth for integrating and using **ArgDigest** in this library.

Metadata
- Source repository: `argdigest`
- Source document: `standards/ARGDIGEST_GUIDE.md`
- Source version: `argdigest@0.5.0`
- Last synced: 2026-02-06

## What is ArgDigest

ArgDigest is a lightweight toolkit for **auditing, validating, and normalizing** function arguments in scientific libraries. It decouples complex input-handling logic from scientific code by providing a standardized orchestration layer.

## Why this matters in this library

- **Consistency**: All functions share the same argument-handling logic.
- **Interoperability**: Coerces heterogeneous inputs (dictionaries, strings, etc.) into canonical internal objects.
- **Diagnostics**: Produces consistent error messages with actionable hints.
- **Traceability**: Integrates with `smonitor` to provide execution breadcrumbs.

## Required files in this library

- `_argdigest.py`: Package-level configuration (digestion source, style, strictness).
- `A/_private/digestion/`: Directory for argument-centric digesters (when using `package` style).
- `A/_private/digestion/argument_names_standardization.py`: (Optional) Standardizer hook.

## Integration Modes

### 1. Argument-Centric (Recommended)
ArgDigest automatically finds "digesters" for each argument name.

```python
# _argdigest.py
DIGESTION_SOURCE = "A._private.digestion.argument"
DIGESTION_STYLE = "package"
```

In the API:
```python
from argdigest import arg_digest

@arg_digest()
def my_function(molecular_system, selection='all'):
    ...
```

### 2. Explicit Mapping
When specific pipelines are needed for specific arguments.

```python
from argdigest import arg_digest

@arg_digest.map(
    item={"kind": "topology", "rules": ["is_valid"]},
    value={"kind": "std", "rules": ["to_bool"]}
)
def process(item, value):
    ...
```

## Mandatory Registration Pattern

To ensure reusability, define custom pipelines in your library:

```python
from argdigest import register_pipeline

@register_pipeline(kind="feature", name="feature.base")
def coerce_feature(obj, ctx):
    # Transformation logic
    return obj
```

## Required behavior (non-negotiable)

1.  **Lazy Digestion**: Digestion only happens when the decorated function is called.
2.  **No Direct Pydantic/Beartype Imports**: Use the native integrations in ArgDigest (`type_check=True` or direct model rules) to keep dependencies soft.
3.  **Use skip_digestion**: All decorated functions should support a `skip_digestion` parameter for performance-critical internal calls.

## SMonitor Integration

ArgDigest is instrumented with `@smonitor.signal(tags=["digestion"])`. Every digestion attempt is traceable.

## Naming conventions

- **Digester functions**: `digest_<argname>(value, caller=None, **kwargs)`.
- **Pipeline names**: `<domain>.<action>` (e.g., `feature.validate`, `std.to_list`).

---
*Document created on February 6, 2026, as the authority for ArgDigest integration.*
