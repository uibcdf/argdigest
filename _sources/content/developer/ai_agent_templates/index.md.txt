# AI Agent Templates

These templates provide ready-to-use instructions for AI agents integrating ArgDigest
into a new library. Choose the style that matches the desired architecture.

The style choice concerns **axis 2**, how per-argument digesters are discovered. Every
template also covers **axis 1**, the function argument contract, which is independent of
the style: a closed signature is held to its own parameters with no declaration, and a
function taking `**kwargs` declares the domain those keywords come from.

## Which template to use

- `package_style`: one file per argument in a digestion package.
- `registry_style`: centralized `argument -> function` mapping.
- `decorator_style`: registration via decorators across modules.
- `mixed_style`: migration periods where multiple styles coexist.

## Validation after template-based integration

After applying a template in a host library:
1. confirm decorated entry points are calling digesters,
2. verify at least one invalid-input path produces expected diagnostics,
3. verify a mistyped keyword is refused rather than ignored,
4. confirm every public callable is decorated, and every `**kwargs` function declares its
   domain — an undeclared one admits anything,
5. confirm docs/examples in the host library match implemented style.

```{toctree}
:maxdepth: 1

package_style
registry_style
mixed_style
decorator_style
```
