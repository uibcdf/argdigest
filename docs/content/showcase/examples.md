# Examples

This section shows two minimal, real libraries embedded in the ArgDigest repository
under `examples/`. They are used for smoke tests and can be copied as templates.

## PackLib (package discovery)

`packlib` demonstrates the **package** discovery style, where digesters live in
`_private/digestion/argument/` and are named `digest_<argument>`.

Key pieces:

- `examples/packlib/basic.py` uses `@digest(config="packlib._argdigest")` to keep defaults in one place.
- `examples/packlib/_private/digestion/normalization/` shows a modular standardizer design
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

- `examples/reglib/_private/digestion/registry.py` defines the mapping.
- `examples/reglib/basic.py` shows dual mode (argument digestion + pipelines) with `@digest(config="reglib._argdigest")`.
