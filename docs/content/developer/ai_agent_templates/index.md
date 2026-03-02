# AI Agent Templates

These templates provide ready-to-use instructions for AI agents integrating ArgDigest
into a new library. Choose the style that matches the desired architecture.

## Which template to use

- `package_style`: one file per argument in a digestion package.
- `registry_style`: centralized `argument -> function` mapping.
- `decorator_style`: registration via decorators across modules.
- `mixed_style`: migration periods where multiple styles coexist.

## Validation after template-based integration

After applying a template in a host library:
1. confirm decorated entry points are calling digesters,
2. verify at least one invalid-input path produces expected diagnostics,
3. confirm docs/examples in the host library match implemented style.

```{toctree}
:maxdepth: 1

package_style
registry_style
mixed_style
decorator_style
```
