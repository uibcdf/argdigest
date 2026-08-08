# Normalization

Normalization renames arguments before anything judges them, so a library can accept the
names its users actually type.

If your users write `residue_index` where the library calls it `group_index`, that is not
a mistake to punish — it is a name worth accepting. Normalization is where you say so,
once, instead of handling it in every function.

## Where it runs, and why aliases survive the function contract

```
bind_arguments -> normalization -> standardizer -> function contract -> digestion
```

Normalization runs **before both** the function contract and the argument digesters, and
the order is deliberate. By the time a contract judges a keyword, an alias has already
become its canonical name, so **declaring a contract never breaks your aliases**.

If the contract ran first it would reject every alias as an unknown argument, turning a
feature built to help users into a wall. A genuine typo, on the other hand, survives
normalization unchanged and is then refused — which is exactly the division of labour you
want: normalization *translates*, the contract *judges*.

## Declaring aliases

Aliases are data. Drop one module per family of rules into the package named by
`NORMALIZATION_SOURCE`, declaring `table` or `TABLES`:

```python
# mylib/_private/argdigest/normalization/synonyms.py
from argdigest import AliasTable

table = AliasTable(
    aliases={'residue_index': 'group_index', 'residue_indices': 'group_index'},
    description='anatomical synonyms of the canonical names',
)
```

```python
# mylib/_argdigest.py
NORMALIZATION_SOURCE = "mylib._private.argdigest.normalization"
```

That is the whole mechanism. ArgDigest discovers the tables, composes them and applies
them; you never write dispatch logic.

### Scoping a table to one function or a family

```python
AliasTable(applies_to='mylib.basic.compare.compare',
           aliases={'attributes_type': 'attribute_type'})

AliasTable(applies_to='mylib.form.*',          # fnmatch pattern
           aliases={'idx': 'index'})
```

`applies_to` defaults to `"*"`, every caller. **Scope is not a detail.** A name that is
an attribute in one function is often an ordinary parameter in another: renaming
`atom_indices` globally in the reference consumer would have rewritten a real parameter
of every adapter into a name none of them declares. Declare a table globally only when
the alias means the same thing everywhere.

### An alias that depends on another argument

`when` guards a table on the value of another argument in the same call:

```python
AliasTable(applies_to='mylib.basic.get.get', when={'element': 'atom'},
           aliases={'name': 'atom_name', 'index': 'atom_index'})

AliasTable(applies_to='mylib.basic.get.get', when={'element': 'group'},
           aliases={'name': 'group_name', 'index': 'group_index'})
```

So `get(molsys, element='atom', name=True)` asks for `atom_name`, and the same `name`
asks for `group_name` when the element is a group.

It is an equality test, not an expression language, and the tables are written out rather
than generated from a `{element}_{name}` template. That is deliberate: a template accepts
combinations that do not exist. In the reference consumer it produced six attribute names
nothing defines, so `get(molsys, element='atom', order=True)` became a request for
`atom_order` and failed much further downstream. A table declares only what is real, and
the unreal name is refused where it is written.

## How tables compose

- **Most specific first.** An exact caller beats a longer pattern beats `"*"`, so a
  function-scoped alias overrides a global one for the same name.
- **One pass, never a chain.** Once `a` has become `b`, it is not reconsidered. Chaining
  would make the result depend on declaration order, which nobody could reason about.
- **Order is preserved.** Arguments keep the order they were written in.

## Reading the aliases back

```python
from argdigest import describe_normalization
```

It renders the declared tables as plain data. This is the practical reason for declaring
rules rather than writing a callable: the alternative names a function accepts can be
listed in its documentation, instead of living undocumented inside a branch.

## The `standardizer` hook

The original mechanism is still supported and still runs, after the declared tables:

```python
def argument_names_standardization(caller, kwargs):
    ...
    return kwargs
```

Contract: it takes `(caller, kwargs)` and **returns** the mapping. ArgDigest checks both —
the signature when the decorator is built, the return value on each call — and reports a
`StandardizerContractError` naming the standardizer. Forgetting the `return` used to
surface much later as `AttributeError: 'NoneType' object has no attribute 'items'`.

Keep it for a rename that a table cannot state, such as one computed rather than
compared. Prefer a table whenever the rule can be written as one: a table is readable,
reportable, and composes with others.

## Migrating an existing standardizer

Move the rules out one branch at a time. Both mechanisms run, declared tables first, so
the behaviour is preserved at every step and the hook shrinks until it is a no-op — or
until only the cases that genuinely need code are left.

## Next

Continue with [skip_digestion Behavior](skip-digestion.md).
