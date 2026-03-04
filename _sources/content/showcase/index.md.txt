# Showcase

This section provides practical, copy-ready integration scenarios.
Each scenario targets a different digestion architecture.

## Example Catalog

| Showcase | What you will find |
|---|---|
| [Package Style Integration](package-style-integration.md) | One-file-per-argument digestion in `_private/digestion/argument`, plus `_argdigest.py` defaults. |
| [Registry Style Integration](registry-style-integration.md) | Central `argument -> digester` mapping for teams that prefer explicit indexing. |
| [Decorator Style Integration](decorator-style-integration.md) | Co-located digesters for compact modules and plugin-driven extension points. |
| [Mixed Migration Strategy](mixed-migration-strategy.md) | Incremental rollout combining discovery styles while migrating legacy code. |
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
examples.md
quickstart.ipynb
example_integration.ipynb
```
