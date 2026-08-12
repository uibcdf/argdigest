# The passport is two classes, and it admits more than it should

**Found:** 2026-08-12, while preparing `ValidatedPayload` for the public API.
**Impact:** low today, because measurement says no consumer uses the mechanism. High the
moment one does, which is what we were about to invite by publishing it.
**Status:** superseded in design by the value-certification model (see the end); this
report exists so the two defects are on record and so the replacement is checked
against them.

## Defect 1 — two classes with the same name

`ValidatedPayload` is declared twice:

- `argdigest/core/contract.py` — the one the decorator checks with `isinstance`
- `argdigest/contrib/pyunitwizard_support.py` — the one the PyUnitWizard pipelines emit

```
core.contract        : <class 'argdigest.core.contract.ValidatedPayload'>
pyunitwizard_support : <class 'argdigest.contrib.pyunitwizard_support.ValidatedPayload'>
SON LA MISMA         : False
```

The decorator's passport protocol can therefore never match a payload produced by those
pipelines. Two failures follow:

```
core.contract  : digester skipped = True   | unwrapped = True   | body receives ndarray
PUW pipelines  : digester skipped = False  | unwrapped = False  | body receives ValidatedPayload
```

The second column is the dangerous one. The wrapper **reaches the function body** in
place of the array it carries, so any `.shape`, arithmetic or kernel call in that body
fails — or worse, silently operates on the wrong object.

## Defect 2 — the passport is honoured by argument name alone

More serious, and independent of the duplication. `core/decorator.py`:

```python
if argname in payloads:
    digested[argname] = bound.get(argname)   # skip the digester, whichever it is
```

The claim carries `unit`, `dtype`, `ndim` — but **nothing about which verification was
performed**. So a passport issued by MolSysMT's digester for `coordinates` also skips
MolSysViewer's digester for `coordinates`, which may verify entirely different things
and may be stricter. Any library's claim silences every other library's check for the
same argument name.

Nothing enforces that the claim and the skipped digester have anything to do with each
other.

## Reproduction

```python
from argdigest import arg_digest, argument_digest
from argdigest.contrib.pyunitwizard_support import ValidatedPayload as emitted
import numpy as np

calls = []

@argument_digest("coordinates")
def digest_coordinates(coordinates):
    calls.append(coordinates)
    return coordinates

@arg_digest(digestion_style="decorator", strictness="ignore")
def measure(coordinates):
    return coordinates

result = measure(emitted(value=np.zeros((4, 3)), unit="nm", dtype="float64", ndim=2))
assert calls == []                          # fails: the digester ran
assert isinstance(result, np.ndarray)       # fails: the body got the wrapper
```

## How it was found

While exporting `ValidatedPayload` from `argdigest/__init__.py`, which it never was:
`argdigest.ValidatedPayload` did not exist and consumers had to import it from
`argdigest.core.contract`, a private path. Unifying the two classes then made a
previously passing test fail, which is how the second defect surfaced.

## What the exposure actually is

Measured across the suite:

| Repository | Uses of `ValidatedPayload` |
| --- | --- |
| PyUnitWizard | none; it does not depend on ArgDigest |
| MolSysViewer | none |
| MolSysMT | one branch in `digest_coordinates`, guarded by `caller.startswith("molsysmt.lib.structure")` — and **no function under `molsysmt/lib/` is decorated** (0 of 1360), so the branch is unreachable |
| ArgDigest | the PyUnitWizard pipelines and two tests |

So the mechanism is used by nobody, and the two defects have never reached a user. That
is also why they went unnoticed: the duplication is invisible until someone passes a
payload across the two worlds.

## What would fix it

Not a repair of this mechanism. Both defects are consequences of its shape:

- the wrapper changes the value's **type**, which is why it has to be unwrapped, which
  is why the two protocols could disagree about *when*;
- the claim describes the **value** rather than the **verification**, which is why it
  cannot know which digester it is entitled to skip.

The replacement under design certifies a value **by identity** rather than wrapping it,
and binds the claim to the digester that issued it, so a claim can only skip the exact
verification it represents. That closes defect 2 by construction and removes defect 1
along with the wrapper.

Until that lands, this report is the record. Anything that revives the wrapper has to
answer both defects.

## Measurements taken while investigating

| | µs per call |
| --- | ---: |
| `@arg_digest` plumbing, nothing declared | 21.6 |
| `skip_digestion=True` fast path | 1.8 |
| `molsysmt_MolSys.has_attribute`, digested | 65.6 |
| the same, with a passport | 36.1 |
| the same, with `skip_digestion=True` | 7.3 |

The passport recovers roughly half of what `skip_digestion` does, because it skips the
digester but still pays binding, normalization and the contract stages. Where the call
site is under your control, `skip_digestion` is the cheaper tool — a fact that was not
written down anywhere and that the guide implied the opposite of.
