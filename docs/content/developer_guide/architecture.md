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

## Performance Strategy

ArgDigest employs caching at two critical levels to ensure minimal runtime overhead:

1.  **Digester Discovery:** `argument_loader._load_from_package` is memoized to avoid repeated `pkgutil.iter_modules` calls.
2.  **Signature Inspection:** `decorator.get_digester_metadata` caches `inspect.signature` results for all digesters, preventing redundant parsing of function signatures during import.
