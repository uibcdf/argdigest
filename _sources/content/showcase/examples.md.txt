# Examples

This section points to minimal integrations embedded in this repository.
They are intended for manual smoke tests and documentation support.

## PackLib (package discovery)

`packlib` demonstrates the **package** discovery style, where digesters live in
`_private/argdigest/argument/` and are named `digest_<argument>`.

Key pieces:

- `examples/packlib/basic.py` uses `@arg_digest(config="packlib._argdigest")` to keep defaults in one place.
- `examples/packlib/_private/argdigest/normalization/` shows a modular standardizer design
  that supports both declarative aliases and dynamic rules.

Example dynamic rule (from `dynamic_rules.py`):

```python
def normalize_get(caller, kwargs):
    if "name" in kwargs and "element" in kwargs:
        kwargs = dict(kwargs)
        kwargs[f"{kwargs['element']}_name"] = kwargs.pop("name")
    return kwargs
```

## Digester templates

Simple digester:

```python
def digest_atom_index(atom_index, caller=None):
    if isinstance(atom_index, int):
        return [atom_index]
    if isinstance(atom_index, list):
        return atom_index
    raise ArgumentError("atom_index", value=atom_index, caller=caller, message=None)
```

Dependent digester (uses another argument such as `syntax`):

```python
def digest_selection(selection, syntax="MyLib", caller=None):
    if syntax == "MyLib":
        if isinstance(selection, str):
            return selection
        if isinstance(selection, int):
            return [selection]
    raise ArgumentError("selection", value=selection, caller=caller, message=None)
```

## RegLib (registry discovery)

`reglib` demonstrates the **registry** style, where digesters are collected in a
module exposing `ARGUMENT_DIGESTERS`.

Key pieces:

- `examples/reglib/_private/argdigest/registry.py` defines the mapping.
- `examples/reglib/basic.py` shows dual mode (argument digestion + pipelines) with `@arg_digest(config="reglib._argdigest")`.

## Notebooks

Two lightweight notebooks exist for quick demonstrations:

- `docs/content/showcase/quickstart.ipynb`
- `docs/content/showcase/example_integration.ipynb`

Use them as exploratory demos, not as canonical integration contracts.

## Beyond digesters

The examples above exercise the value contract. Two scenarios cover the rest of an
integration:

- [Integrating an API with `**kwargs`](kwargs-api-integration.md) — declaring a `Domain`
  and a `FunctionContract` for the one case a signature cannot cover.
- [Migrating a standardizer to alias tables](standardizer-to-alias-tables.md) — turning a
  chain of `if caller == ...` renames into declared data.

When adapting any example below, add one check that a mistyped keyword is refused. A
closed signature gives you that with nothing declared, and it is the cheapest guard
against a call running with the default and returning a plausible wrong answer.
