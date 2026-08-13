# Showcase

This section provides practical, copy-ready integration scenarios.

The first four target a different **digestion architecture** — how per-argument digesters
are discovered. The last two cover the other half of an integration: declaring what each
function accepts, and declaring the alternative names users may type.

## Example Catalog

| Showcase | What you will find |
|---|---|
| [Package Style Integration](package-style-integration.md) | One-file-per-argument digestion in `_private/argdigest/argument`, plus `_argdigest.py` defaults. |
| [Registry Style Integration](registry-style-integration.md) | Central `argument -> digester` mapping for teams that prefer explicit indexing. |
| [Decorator Style Integration](decorator-style-integration.md) | Co-located digesters for compact modules and plugin-driven extension points. |
| [Mixed Migration Strategy](mixed-migration-strategy.md) | Incremental rollout combining discovery styles while migrating legacy code. |
| [Integrating an API with `**kwargs`](kwargs-api-integration.md) | Declaring a `Domain` and a `FunctionContract` for the one case that cannot be covered by a signature. |
| [Migrating a standardizer to alias tables](standardizer-to-alias-tables.md) | Turning a chain of `if caller == ...` renames into declared data, with the two mistakes the real migration produced. |
| [Examples and Notebooks](examples.md) | Minimal embedded libraries and notebooks for manual smoke validation. |
| [Showcase Notebook: Quickstart](quickstart.ipynb) | Minimal notebook showing a first decorated function and immediate behavior. |
| [Showcase Notebook: Example Integration](example_integration.ipynb) | Notebook with a compact integration flow including pipeline registration. |

```{toctree}
:maxdepth: 1
:hidden:

package-style-integration.md
registry-style-integration.md
decorator-style-integration.md
mixed-migration-strategy.md
kwargs-api-integration.md
standardizer-to-alias-tables.md
examples.md
quickstart.ipynb
example_integration.ipynb
```
