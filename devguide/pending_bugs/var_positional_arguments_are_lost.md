# `@digest` cannot carry a `*args` function

**Found:** 2026-08-12, from MolSysViewer, against ArgDigest 0.11.0.
**Impact:** any positional call to a decorated `*args` function raises. Silent for
keyword-only callers, which is why it can sit unnoticed in a released library.

> **Fixed 2026-08-12**, unreleased. `core/utils.build_call` reconstructs the call shape
> and `core/decorator._invoke` uses it at both call sites; `DigestionPlan.requires_call_shape`
> decides once per decorated function whether a signature needs it, so a signature with
> neither `*args` nor `/` keeps the single dict unpack it had. Held by
> `tests/test_call_shape.py` (18 tests). The suspected positional-only failure was
> confirmed and is fixed by the same change. The var-positional digestion semantics —
> one tuple, one digester, named for the parameter — are now documented in `SPEC.md`
> §4.4 and in `standards/ARGDIGEST_GUIDE.md` §5. **MolSysViewer's exemption test can be
> retired once this ships.**

## What happens

`arg_digest` binds the call, digests the bound arguments, and then invokes the wrapped
function **by keyword only** (`core/decorator.py:353` and `:519`):

```python
return fn_to_wrap(**bound)
```

A var-positional parameter has no keyword form. Two failures follow from the same line:

1. **Positional calls raise.** Measured on a decorated
   `def add_pharmacophore_features(self, *args, skip_digestion=False, **kwargs)`:

   ```
   TypeError: too many positional arguments
   ```

2. **Even bound, the tuple would not arrive.** `bound["others"] = (a, b)` passed as
   `**bound` becomes the keyword `others=(a, b)`, which a `*others` parameter cannot
   receive — it lands in `**kwargs` if one exists, and raises if not.

The second is the more dangerous shape, because a function that does not check its
operands would simply act on nothing.

## Reproduction

```python
from argdigest import digest

@digest()
def combine(*items, tag=None, skip_digestion=False):
    return items

combine("a", "b")          # TypeError: too many positional arguments
combine(tag="x")           # fine — never touches the var-positional
```

## How it was found

MolSysViewer decorated three region boolean-composition methods
(`Region.difference` / `intersection` / `union`, each `*others`). Their bodies open with
`if not others: raise TypeError(...)`, so the tests failed loudly and the cause was
visible.

The same decoration had **already** been applied to
`molsysviewer/shapes/pharmacophore.py:add_pharmacophore_features`, where nothing checks,
and it went unnoticed because the only test that calls it passes keywords *and*
`skip_digestion=True`, which bypasses digestion entirely. That function is public and
documented in a notebook; positional callers get the `TypeError` today.

## What would fix it

Reconstruct the call rather than flattening it to keywords. `inspect.BoundArguments`
already carries the split:

```python
bound_arguments.arguments.update(digested)
return fn_to_wrap(*bound_arguments.args, **bound_arguments.kwargs)
```

That preserves var-positional, positional-only (`/`) and keyword-only parameters, all
three of which the current form loses or mishandles. **Positional-only parameters are
worth checking while this is open**: `fn(**bound)` cannot pass them either, so a decorated
function using `/` is likely broken in the same way and nobody has looked.

The digestion of a var-positional is a separate question this does not settle: ArgDigest
binds `*others` as one tuple and asks for one digester named `others`, which is a
defensible choice but is not documented anywhere. Whatever is decided, say it — a library
author currently discovers it from a `DigestNotDigestedWarning`.

## Meanwhile

**Do not decorate a function that takes `*args`.** MolSysViewer now enforces that with a
test (`tests/test_public_api_inventory.py::test_no_decorated_callable_takes_var_positional`)
and records the affected callables as deliberately undigested, with this document as the
reason. That exemption disappears when this is fixed.
