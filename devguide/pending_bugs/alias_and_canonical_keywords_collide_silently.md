# Alias and canonical keywords collide silently

**Found:** 2026-08-14, while auditing MolSysViewer's adoption of the declarative
normalization API against ArgDigest 0.12.0 and current `main` (`0514b86`).

**Impact:** high. A call that supplies an alias and its canonical keyword loses one value
without an exception or warning. Which value survives depends on keyword insertion
order, so reordering an otherwise equivalent call can change a scientific result.

**Status:** active. The runtime correction and direct regressions are complete; closure
still requires the downstream MolSysMT and MolSysViewer rechecks.

**Execution checkpoint — segment 1, 2026-08-14:** the collision contract is now
executable in `tests/test_normalization_rules.py`. Four cases cover both insertion orders
of alias plus canonical, two aliases converging on one target, and the decorated-call
boundary. They are deliberately `xfail(strict=True)`: the suite remains green while the
known defect is present, and any implementation that starts satisfying the contract
must remove the markers in the same atomic segment or fail with an unexpected pass. No
runtime, exception hierarchy or public API changed in this segment.

**Implementation checkpoint — segment 2, 2026-08-14:** collision detection now runs
after table resolution but before the normalized dictionary is rebuilt. It groups every
supplied source by its resolved target and raises the existing catalog-backed
`ArgumentConsistencyError` (`ARG-ERR-CONTRACT-003`) whenever a target has more than one
source. The diagnostic carries the caller and canonical target in structured context and
names every conflicting source. A dedicated exception was rejected because this is
already an inter-argument consistency violation and no caller needs another public type.
All strict expected-failure markers were removed; the regression also rejects equal
values and covers aliases contributed by tables of different specificity. User and agent
documentation now state that aliases are alternatives.

## Original behavior

Before segment 2, `apply_normalization()` recorded `coords -> coordinates`, then rebuilt the mapping
with a dictionary comprehension:

```python
return {renames.get(name, name): value for name, value in bound.items()}
```

If `bound` already contains `coordinates`, both entries produce the same output key.
Python keeps the value inserted last and silently discards the other one:

```python
from argdigest import AliasTable
from argdigest.core.normalization import NormalizationRegistry, apply_normalization

registry = NormalizationRegistry([
    AliasTable(aliases={"coords": "coordinates"}),
])

apply_normalization(
    registry,
    "pkg.f",
    {"coords": True, "coordinates": False},
)
# {'coordinates': False}

apply_normalization(
    registry,
    "pkg.f",
    {"coordinates": False, "coords": True},
)
# {'coordinates': True}
```

Those outputs reproduce commit `0514b86`; current `main` raises
`ArgumentConsistencyError` for both calls before rebuilding the mapping.

The same defect applies when two simultaneously supplied aliases target one canonical
name. It is not limited to a source/canonical pair or to one table: caller-specific,
pattern and global tables compose before the mapping is rebuilt.

## Downstream evidence

MolSysViewer imports MolSysMT's attribute aliases for query wrappers. Against the
checkouts used to file the report, both calls were accepted but returned different
results solely because the two keywords were reversed:

```python
view.get(element="atom", atom_names=True, atom_name=False)
# []

view.get(element="atom", atom_name=False, atom_names=True)
# ['H1', 'CH3', ...]
```

The query itself is valid and both names are individually supported. The ambiguity is
created by supplying them together, but ArgDigest currently turns that ambiguity into a
deterministic-looking result instead of refusing it.

## Why this is dangerous

- The call completes successfully and returns plausible data.
- The function contract sees only the already-collapsed canonical mapping and cannot
  detect that two user inputs existed.
- Argument digesters also see only the surviving value.
- Keyword order is not a scientific conflict-resolution policy.
- Comparing values before deciding would not solve the contract: NumPy and quantity
  equality may be array-valued, expensive, unit-sensitive or undefined, and two equal
  values still express the same argument twice.

This is therefore more serious than rejecting an alias or producing a poor diagnostic.
It is silent loss of user input at the validation boundary.

## Root cause

Normalization records renames by source name but never checks whether the resulting
target names are unique. The final dictionary comprehension is the first point at which
the collision becomes concrete, and ordinary dictionary semantics resolve it implicitly.

The existing tests cover:

- self-alias rejection at declaration time;
- specificity between tables for one source name;
- one-pass rather than chained renaming; and
- insertion-order preservation when targets remain distinct.

None supplies two source entries that resolve to the same target.

## Required behavior

Reject a call whenever two supplied input names resolve to one output name. This includes:

1. an alias and its canonical name;
2. two aliases with the same canonical target;
3. collisions produced by tables of different specificity; and
4. a declared alias colliding with a name emitted by the optional standardizer, if that
   composition can reach the same state.

The exception must name the caller, canonical target and every conflicting source name.
`ArgumentConsistencyError` is the closest existing catalog-backed type; a dedicated
`AliasConflictError` is justified only if callers need to distinguish this condition
programmatically. The decision should be made before adding a new public exception to
the 1.0 API.

Reject the call even when the two values compare equal. This keeps the rule cheap,
deterministic and valid for arrays, quantities and objects with unusual equality
semantics.

## Acceptance criteria

- Direct normalization tests cover both keyword orders for alias plus canonical and
  raise the same catalog-backed exception.
- Two distinct aliases targeting the same canonical name are also rejected.
- Non-colliding aliases retain insertion order and existing one-pass behavior.
- Table specificity still decides which target applies to one source; it never decides
  which of two supplied values survives.
- An end-to-end decorated `**kwargs` function rejects the conflict before its body and
  before argument digestion.
- User and developer documentation state that aliases are alternatives, not additional
  independently meaningful arguments.
- The MolSysViewer reproduction is added as downstream evidence or rechecked after the
  ArgDigest fix lands.

## What was refuted

Treating “last keyword wins” as a documented policy was rejected. It is inherited from a
dictionary implementation detail and makes refactoring call order behavior-changing.

Keeping the canonical spelling unconditionally was also rejected. It would be
deterministic but would still hide a contradictory user input, and determining which
entry was canonical becomes less obvious when two aliases collide.

Accepting both when values compare equal was rejected because equality is not a safe or
uniform predicate over scientific values and because duplicate intent remains ambiguous.

Self-alias handling is a separate, already guarded declaration error. This report is
about two distinct supplied names converging on one target during a call.

## Resolution

Pending downstream closure. Segments 1 and 2 are complete. Segment 3 must run the full
ArgDigest suite and the focused MolSysMT/MolSysViewer alias surfaces, verify that the
compact diagnostic is sufficient, and update any downstream contract prose. Move this
report to `devguide/solved_bugs/` only after those rechecks are complete.
