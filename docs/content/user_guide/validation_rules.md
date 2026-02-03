# Validation rules

ArgDigest supports two complementary rule systems:

- **Argument digesters**: per-argument functions named by the argument or registered explicitly.
- **Pipelines**: reusable rules grouped by `kind` and referenced by name.

## Argument digesters

Argument digesters are normal Python functions. They may coerce values, validate inputs,
raise errors, or return a transformed value.

### Simple case (single-argument digester)

```python
def digest_atom_index(atom_index, caller=None):
    if isinstance(atom_index, int):
        return [atom_index]
    if isinstance(atom_index, list):
        return atom_index
    raise ArgumentError("atom_index", value=atom_index, caller=caller, message=None)
```

### Dependent case (uses other arguments)

Some digesters depend on other arguments passed to the function. For example, a `selection`
digester may adapt its behavior based on the `syntax` argument.

```python
def digest_selection(selection, syntax="MyLib", caller=None):
    if syntax == "MyLib":
        if isinstance(selection, str):
            return selection
        if isinstance(selection, int):
            return [selection]
    raise ArgumentError("selection", value=selection, caller=caller, message=None)
```

ArgDigest resolves these dependencies automatically by digesting required arguments first.

```python
from argdigest import argument_digest

@argument_digest("selection")
def digest_selection(selection, caller=None, syntax=None):
    if selection is None:
        return "all"
    return selection
```

## File-based template (package style)

For the `package` discovery style, each argument has a Python file named after the argument,
and the function name must follow `digest_<argument>`.

Example structure:

```
_private/digestion/argument/
  selection.py
  atom_index.py
```

Example file (`selection.py`):

```python
def digest_selection(selection, syntax="MyLib", caller=None):
    ...
```

ArgDigest will:

- pass the argument value as the first parameter,
- inject `caller` if present,
- resolve other parameters (like `syntax`) from the function call.

## Digester discovery

Argument digesters can be discovered in multiple ways, depending on how a library is organized.
Configure discovery with `digestion_source` and `digestion_style` in `@arg_digest`:

```python
@arg_digest(
    digestion_source="mylib._private.digestion.argument",
    digestion_style="package",
    strictness="warn",
)
def get(molecular_system, selection=None, skip_digestion=False):
    return molecular_system, selection
```

Discovery modes:

- `registry`: use `ARGUMENT_DIGESTERS` from a module.
- `package`: scan a package for functions named `digest_<argument>`.
- `decorator`: use `@argument_digest` registration.
- `auto`: combine sources in a safe default order.

## Pipelines by kind

```python
from argdigest import register_pipeline

@register_pipeline(kind="feature", name="feature.base")
def feature_base(obj, ctx):
    if not hasattr(obj, "feature_id"):
        raise ValueError("Missing feature_id")
    return obj
```

## Strictness for undigested arguments

When using argument digesters, `strictness` controls what happens if an argument has no
associated digester:

- `warn` (default): emit a warning.
- `error`: raise a `DigestNotDigestedError`.
- `ignore`: do nothing.
