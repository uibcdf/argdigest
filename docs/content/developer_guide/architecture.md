# Architecture

ArgDigest is organized around three core concepts:

- **Argument digestion**: per-argument digesters discovered from user libraries.
- **Pipelines**: reusable rules registered by `kind` and executed in order.
- **Context and errors**: structured data and exceptions for consistent diagnostics.

Key modules:

- `argdigest/core/decorator.py`: `@digest` implementation and execution flow.
- `argdigest/core/argument_loader.py`: discovery of argument digesters.
- `argdigest/core/argument_registry.py`: decorator-based digester registry.
- `argdigest/core/registry.py`: pipeline registry and execution.
- `argdigest/core/context.py`: call context container.
- `argdigest/core/errors.py`: error and warning classes.
