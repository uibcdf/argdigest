# Error handling

ArgDigest provides structured errors to make digestion failures easier to debug.

## Rich Error Context

Starting from v0.2, exceptions raised by ArgDigest carry rich context information to help debugging.
When printed, they display a structured message:

```text
Argument 'my_arg' from 'mylib.func' has no digester
  Function: mylib.func
  Argument: my_arg
  Value: 'invalid_value'
  Hint: Check if the argument name is correct or if a digester is registered.
```

The exception object contains a `context` attribute (SimpleNamespace) with:
- `function_name`: The fully qualified name of the function.
- `argname`: The name of the argument being processed.
- `value`: The raw value passed to the function.
- `all_args`: A dictionary of all bound arguments.

## Dependency Cycles

If ArgDigest detects a circular dependency between arguments (e.g., `a` requires `b`, and `b` requires `a`), it raises a `DigestNotDigestedError` with the full path of the cycle:

`Cyclic dependency detected: a -> b -> a`

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
    process_data(bad_input)
except DigestError as e:
    print(f"Error in {e.context.function_name}: {e}")
    if e.hint:
        print(f"Suggestion: {e.hint}")
```
