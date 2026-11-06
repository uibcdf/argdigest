# Architecture

ArgDigest is organized around three core concepts:

- **Argument digestion**: per-argument digesters discovered from user libraries.
- **Pipelines**: reusable rules registered by `kind` and executed in order.
- **Context and errors**: structured data and exceptions for consistent diagnostics.

Key modules:

- `argdigest/core/decorator.py`: `@arg_digest` implementation and execution flow.
- `argdigest/core/argument_loader.py`: discovery of argument digesters. Uses `functools.lru_cache` to prevent redundant package scanning.
- `argdigest/core/argument_registry.py`: decorator-based digester registry.
- `argdigest/core/registry.py`: pipeline registry and execution.
- `argdigest/core/context.py`: call context container.
- `argdigest/core/errors.py`: error and warning classes.

## The two axes

ArgDigest runs two independent checks over a call, in this order:

```
bind_arguments -> standardizer -> function contract (axis 1) -> digestion (axis 2)
```

**Axis 1** answers whether a function may receive an argument at all. It is resolved from
declared `FunctionContract`s, most specific first: exact caller, then the longest matching
`caller_pattern`, then a default that holds a closed signature to its own parameters and
lets a `**kwargs` function admit anything.

**Axis 2** answers whether an argument's value is valid, through per-argument digesters.

The order is forced by dependencies. The contract runs **after** the standardizer, so an
alias that has just become its canonical name is never mistaken for a typo; and **before**
digestion, because validating the value of an argument that should not be there is wasted
work ending in a confusing failure. `bind_arguments` sets aside the keywords a closed
signature cannot take and hands them to the contract stage rather than discarding them —
a binding step must not make a policy decision, which is precisely the defect axis 1 was
introduced to repair.

## Performance Strategy

ArgDigest employs caching at two critical levels to ensure minimal runtime overhead:

1.  **Digester Discovery:** `argument_loader._load_from_package` is memoized to avoid repeated `pkgutil.iter_modules` calls.
2.  **Signature Inspection:** `decorator.get_digester_metadata` caches `inspect.signature` results for all digesters, preventing redundant parsing of function signatures during import.
