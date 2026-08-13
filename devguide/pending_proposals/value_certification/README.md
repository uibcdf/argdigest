# Proposal: certify a digested value by identity

**Status:** built, measured, working — and **not adopted** (2026-08-13).
**Code:** [`canonical.py`](canonical.py) and [`test_canonical.py`](test_canonical.py),
verbatim, 27 tests green when they were removed from the package.
**Replaces:** `ValidatedPayload`, removed in
[`../../solved_bugs/the_passport_is_two_classes_and_admits_too_much.md`](../../solved_bugs/the_passport_is_two_classes_and_admits_too_much.md).

This is not a design waiting to be finished. It is a finished design that was declined,
and the reasons are the point of keeping it.

## The problem it solves

Digesters that *convert* are expensive — a unit conversion, an `asarray` over a large
frame, an assessment of which form an object is in. Running one again on a value that
has not changed is waste.

`skip_digestion=True` covers the case where you control the call site. It does not cover
the one where the user does:

```python
coords  = msm.get(molsys, coordinates=True)                      # canonical already
com     = msm.structure.get_center_of_mass(molsys, coordinates=coords)
rmsd    = msm.structure.get_rmsd(molsys, coordinates=coords, reference=ref)
```

Those are public boundaries, so digestion belongs there — but the value came out of the
library's own API and is re-canonicalized on every call. Asking the user to pass
`skip_digestion` would hand an architectural decision to the person least able to make
it.

## What it does

`certify(value, by=..., **attributes)` records that a value satisfies a verification and
returns **the same object** — no wrapper, no type change, nothing for a function body to
know about. `claim_for(value, by=...)` asks whether the claim is there.

Two properties make it safe rather than merely fast:

- **A claim names the verification it represents.** Not "this value is fine" but "this
  value satisfies *this digester*". The mechanism it replaces was honoured by argument
  *name*, so a claim issued by one library silenced another library's digester for the
  same name.
- **Modification costs the claim.** `guard="form"` (the default) revokes on reshape or
  retype and touches nothing, which is right for the overwhelming majority of digesters:
  MolSysMT rotates coordinates in place, and rotating nm float64 (n,3) leaves it nm
  float64 (n,3). `guard="frozen"` is opt-in for a guarantee about content, and freezes
  the array so that mutating it requires an explicit unfreeze — which is observable, and
  revokes destructively so refreezing cannot resurrect it.

| | measured |
|---|---:|
| `certify(...)` | 3.5 µs, flat with size |
| `claim_for(v, by=...)` | 0.46 µs |
| no claim held (the common case) | 0.18 µs |
| what it avoids: coercing 5000 atoms | 1496 µs |

## Why it was declined

**It asks every digester author to learn three concepts** — `by`, `guard`, `source` —
plus a global registry with its test-isolation consequences, and debugging where the
call site no longer tells you whether digestion will run.

**No consumer had the problem.** Measured across MolSysMT, MolSysViewer and
PyUnitWizard, the mechanism it replaces had zero users. The one performance defect
actually measured in the ecosystem was a placement bug
([uibcdf/molsysmt#147](https://github.com/uibcdf/molsysmt/issues/147)) that no
certification of any design would have fixed.

**And the problem is not ours.** This was the finding that settled it. The reason a
digester cannot cheaply short-circuit is that asking *"is this quantity already in
nanometers?"* costs more than converting it:

| | 5000 elements |
|---|---:|
| `puw.get_unit(q)` | 363 µs |
| `puw.check(q, unit='nm')` | 887 µs |
| `q.units` — the pint attribute underneath | **0.88 µs** |

The capability exists at the bottom; PyUnitWizard does not expose it. Filed as
`uibcdf/pyunitwizard` → `devguide/pending_proposals/cheap_canonicity_predicate.md`.

With a ~1 µs predicate, a digester short-circuits locally in two lines, with no
mechanism, no registry, and nothing new to learn. **This whole module exists to avoid
asking a question that should be cheap.**

## When to reconsider

Adopt this only when all three hold:

1. A consumer has a **measured** chain where the same canonical value is re-digested
   across call sites it does not control, with the cost attributed.
2. The cheap predicate in PyUnitWizard either landed and was not enough, or was refused.
3. The cost is not explained by digestion sitting somewhere it should not — check
   [#147](https://github.com/uibcdf/molsysmt/issues/147) first, because that was the
   answer last time.

If those hold, the design here is likely still the right shape, but **do not assume the
details survive**. `guard="form"` as the default, the freezing turnstile and the
numpy-specific handling were all chosen against a hypothetical use case. A real one may
want something else, and starting from the measurement rather than from this code is the
better path.

## Restoring it

```bash
git mv devguide/pending_proposals/value_certification/canonical.py argdigest/core/canonical.py
git mv devguide/pending_proposals/value_certification/test_canonical.py tests/test_canonical.py
```

The module has no imports from the rest of `core`, so it stands alone. Wiring it into the
decorator is the part that was never written: `gut()` would consult
`claim_for(value, by=fn_digest)` before running a digester, and skip it on a hit.
