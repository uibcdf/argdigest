# SMonitor integration

ArgDigest uses **SMonitor** to standardize warnings, errors, and diagnostics.

## Files

- `argdigest/_smonitor.py`
- `argdigest/_private/smonitor/catalog.py`
- `argdigest/_private/smonitor/meta.py`

## Emission pattern

```python
from smonitor.integrations import emit_from_catalog
from argdigest._private.smonitor import CATALOG, META, PACKAGE_ROOT

emit_from_catalog(
    CATALOG["missing_digester"],
    package_root=PACKAGE_ROOT,
    meta=META,
    extra={"argname": argname},
)
```

## Guidance

- Keep user messages explicit and actionable.
- Keep hints concise and link to docs/issues when useful.
- Avoid hardcoded messages outside the catalog.

## Contributor rule

If a new warning/error path is added:
1. update catalog entries,
2. keep message fields contract-consistent,
3. update docs where user-visible behavior changes.
