# Migrating a standardizer to declared alias tables

Use this pattern when a library already renames arguments through the `standardizer` hook
and the hook has grown a chain of `if caller == ...` branches.

The migration below is the real one performed on MolSysMT, including the two mistakes it
produced, because both are easy to repeat.

## Before

One callable, holding every rule:

```python
def argument_names_standardization(caller, kwargs):
    from mylib.attribute import _attribute_synonyms

    if caller == 'mylib.basic.get.get':
        element = kwargs['element']
        if 'name' in kwargs:
            kwargs = _replace_key(kwargs, 'name', element + '_name')
        if 'index' in kwargs:
            kwargs = _replace_key(kwargs, 'index', element + '_index')
        ...
        for arg in kwargs:
            if arg in _attribute_synonyms:
                kwargs = _replace_key(kwargs, arg, _attribute_synonyms[arg])

    elif caller == 'mylib.build.mutate.mutate':
        ...
    return kwargs
```

It works. What it cannot do is be read: the alternative names a function accepts are not
listed anywhere, they are consequences of a branch.

## After

```text
mylib/_private/argdigest/normalization/
  attribute_synonyms.py    # the global table, scoped to the functions that take them
  get_element_names.py     # one table per element, guarded by `when`
  caller_aliases.py        # the per-function one-offs
```

```python
# attribute_synonyms.py
from argdigest import AliasTable
from mylib.attribute import _attribute_synonyms

_ATTRIBUTE_TAKING_CALLERS = (
    'mylib.basic.get.get',
    'mylib.basic.contains.contains',
    'mylib.basic.is_composed_of.is_composed_of',
)

TABLES = [
    AliasTable(applies_to=caller, aliases=dict(_attribute_synonyms))
    for caller in _ATTRIBUTE_TAKING_CALLERS
]
```

```python
# get_element_names.py
TABLES = [
    AliasTable(applies_to='mylib.basic.get.get', when={'element': 'atom'},
               aliases={'name': 'atom_name', 'index': 'atom_index',
                        'id': 'atom_id', 'type': 'atom_type'}),
    AliasTable(applies_to='mylib.basic.get.get', when={'element': 'bond'},
               aliases={'index': 'bond_index', 'id': 'bond_id',
                        'type': 'bond_type', 'order': 'bond_order'}),
    ...
]
```

Add `NORMALIZATION_SOURCE` to `_argdigest.py` and the hook can shrink to nothing.

## Two mistakes worth not repeating

**Do not widen the scope while you migrate.** The synonyms were applied inside three
functions, and declaring them globally looked like an improvement. It broke 76 tests:
`atom_indices` is an attribute synonym, but it is also a real parameter of every form
adapter, and the global table rewrote it into `atom_index`, which no adapter declares.
A name that is an attribute in one function is often an ordinary parameter in another.

**Do not generate the tables from a template.** `{element}_{name}` is far shorter than
writing out twenty-eight entries, and it accepts names that do not exist: it produced
`atom_order`, `chain_order` and `bond_name` among others. Asking for `order` on an atom
became a request for `atom_order` and failed somewhere downstream instead of at the name.
Derive the tables by crossing the library's own element list with its attribute
catalogue, so every entry is real and none is invented.

## Migrating safely

Both mechanisms run — declared tables first, then the hook — so rules can move one branch
at a time with behaviour preserved at every step.

Keep the hook only for a rename a table cannot state, such as one computed rather than
compared. MolSysMT ended with none, and now declares no `STANDARDIZER` at all, which is
the outcome to aim for.

## What you gain

- The aliases are a list, not a control flow.
- `describe_normalization` reads them back, so a function's documentation can state the
  alternative names it accepts.
- Tables compose: two modules add aliases without touching each other.
- Declaring a function contract never breaks them, because normalization runs first.

## Smoke check

1. Every alias that worked before still works.
2. A genuine typo is refused rather than translated.
3. A name the old template would have invented is now refused at the name.
4. The hook is a no-op, or holds only what a table cannot express.
