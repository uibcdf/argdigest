# Error handling

ArgDigest provides structured errors to make digestion failures easier to debug.

## Core error types

- `DigestError`: base class for all ArgDigest errors.
- `DigestTypeError`: wrong type.
- `DigestValueError`: invalid value.
- `DigestInvariantError`: semantic rule violation.
- `DigestNotDigestedError`: argument has no digester and `strictness='error'`.
- `DigestNotDigestedWarning`: warning when `strictness='warn'`.

## Example

```python
from argdigest import DigestError

try:
    ...
except DigestError as e:
    print(e)
```
