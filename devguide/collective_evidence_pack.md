# Collective Evidence Pack

This document is the cross-repo handoff artifact for collective validation with:
- `../smonitor`
- `../depdigest`
- `../pyunitwizard`

## What this is

`collective_evidence_pack.md` is the canonical checkpoint record for ArgDigest:
- local evidence already validated in this repository,
- required cross-library E2E evidence,
- pending items that cannot be closed locally.

## How to use this file

1. Before each RC/stabilization checkpoint:
- refresh local evidence and references.

2. During cross-repo synchronization:
- compare status notes across all four repositories.

3. At go/no-go decisions:
- use decision placeholders to record owner, date, blockers, and evidence links.

## How to update this file

1. Update metadata (`Date`, `baseline`, `head reference`).
2. Refresh local quality and integration evidence.
3. Keep only reproducible, in-repo references.
4. Do not mark collective closure from local-only evidence.

Date: `2026-03-04`
ArgDigest baseline: `0.9.x` RC consolidation window
ArgDigest head reference for this pack: `aaab957` (`0.9.2`)

## 1. Local quality baseline (ArgDigest)

- Source status references:
  - `devguide/0.9.x_checklist.md`
  - `devguide/1.0.0_checklist.md`

## 2. Contract evidence index (ArgDigest)

Use this section to keep concrete, local references for:
- shared collective error-path E2E module: `tests/e2e/test_collective_error_path.py`,
- pipeline orchestration and validation contracts,
- unit error mapping from PyUnitWizard into ArgDigest errors,
- diagnostics profile behavior (`user` vs `dev`/`qa`),
- inspection caching/performance behavior.

## 3. Collective E2E target scenario (must be validated across repos)

Goal:
- PyUnitWizard-originated unit/conversion failures are mapped to ArgDigest
  contract errors and emitted with stable SMonitor diagnostics plus DepDigest
  remediation hints when relevant.

Minimum acceptance evidence:
- reproducible command/workflow,
- captured output/events or artifact,
- per-library references to tests/commits proving the path.

## 4. Shared status template

```md
Status note (YYYY-MM-DD):
- smonitor: <done locally|in progress|blocked|pending> (<reference>)
- depdigest: <done locally|in progress|blocked|pending> (<reference>)
- argdigest: <done locally|in progress|blocked|pending> (<reference>)
- pyunitwizard: <done locally|in progress|blocked|pending> (<reference>)
- collective validation: <pending|in progress|done> (<evidence>)
```

## 5. Status note (2026-03-04)

- smonitor: in progress (`0.11.4-16-ge0e1a8c`, profile-parity and collective finality still open)
- depdigest: in progress (`0.10.0-1-gcb93e7f`, stabilization line advanced but collective closure pending)
- argdigest: done locally (`0.9.2`, RC consolidation closed and go/no-go pack prepared)
- pyunitwizard: done locally (`0.21.1-1-g9fd9b46`, RC close completed and maintenance patch released)
- collective validation: in progress (shared E2E path is green, but `../molsyssuite/devguide/collective_v1_checklist.md` finality criteria are not closed)

## 6. Pending collective closures (from ArgDigest perspective)

- final collective approval of criteria #2 and #3 in `../molsyssuite/devguide/collective_v1_checklist.md`,
- explicit cross-repo evidence links in the final decision log (owner/date/blockers/resolution),
- criterion #1 closure once all four libraries reach `>=1.0.0`.

## 7. Decision log placeholders

- `go/no-go owner`:
- `date`:
- `collective evidence links`:
- `open blockers`:
- `resolution plan`:
