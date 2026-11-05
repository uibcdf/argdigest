---
summary: Receive the accepted SMonitor nested-signal observation correction.
issue: uibcdf/argdigest#49
status: blocked
opened: 2026-11-04
closed:
verification: measured
area: [diagnostics, integration, receiving]
guard:
normative:
blocked_by: [uibcdf/smonitor#59]
supersedes: []
---

# Receive nested-signal correction

## What

The incoming owner handoff arrived while #43–#48 were being completed. SMonitor
owns the reported filtered-inner-DEBUG suppression of an outer ERROR under
`uibcdf/smonitor#59`; suite coordination is `uibcdf/molsyssuite#163` and the
requesting consumer is `uibcdf/dockingmt#19`. No public corrected provider
version, minimum or installed receiving artifact is selected by this task.

## How

Keep ArgDigest's normal signal composition. Do not reorder consumer decorators,
clear private flags, copy provider logic, raise production verbosity or update
diagnostic baselines automatically. Once the owner provides an accepted exact
provider/public file, compare filtered DEBUG, accepted DEBUG, nested ERROR,
disabled/silenced diagnostics, catalog/native exceptions, configuration and
restrictive capture. Preserve exception identity, args and causes.

A bounded source control on the actual editable SMonitor visible in the shared
environment already observes outer ERROR at WARNING threshold and DEBUG at
DEBUG threshold, with the same ValueError object/args/cause in both cases.
This is a positive source-composition control, not a reproduction of the old
provider failure and not a public receiving claim. ArgDigest source is 7fdf726.
The provider HEAD observed for that invocation was
`82dad5a7e26e0fba712e30657a6739188d770d79`; a concurrent owner commit then advanced
it to `7fad8f5` with additional tests. The runtime file hashes captured are:

- `smonitor/core/decorator.py`:
  `04bbc6b5b9e37c5ec98975ea868f70c4aa2a258d3f747afa8a2c6c72a97f22ab`;
- `smonitor/core/manager.py`:
  `bc7ae0cd5e01f4e075483edadd474ac3b9f782d20cf71e333de1f11c38c1e71a`.

The shared clone and environment were not changed by this control. The owner's
original baseline/private-wheel comparisons remain in the linked provider issue.
This report stays blocked for the accepted published-provider decision and
required installed receiving, rather than treating a local source control as
completed adoption.

## Why

Additional outer diagnostic observations can change QA identities/counts without
changing native failures. The provider must own acceptance/publication; ArgDigest
owns its subsequent receiving tests and dependency/guide decisions. The follow-up
is independent of the completed #43–#48 source repairs and the #9 typing deferral.
