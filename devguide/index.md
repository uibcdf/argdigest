# Devguide Index

This directory contains internal development guidance, release planning, and
operational notes for ArgDigest.

## Contents

- `DEVELOPER_GUIDE.md`: contributor technical orientation and core engineering rules.
- `ROADMAP.md`: staged release plan from current series to `1.0.0`.
- `0.6.x_checklist.md`: release gate for integration hardening and closure criteria.
- `0.7.x_checklist.md`: API freeze gate and contract-lock tasks.
- `0.8.x_checklist.md`: release-candidate readiness gate before `1.0.0`.
- `0.8.0_release_notes_draft.md`: draft notes for the `0.8.0` RC milestone.
- `0.9.x_checklist.md`: final RC consolidation gate before `1.0.0`.
- `0.9.0_release_notes_draft.md`: draft notes for the `0.9.0` consolidation RC.
- `0.9.1_release_notes_draft.md`: draft notes for the `0.9.1` stabilization patch.
- `0.9.2_release_notes_draft.md`: draft notes for the `0.9.2` final pre-1.0 stabilization checkpoint.
- `0.10.0_release_notes_draft.md`: the function argument contract (axis 1) and its
  deliberate pre-`1.0.0` breaking change.
- `0.12.0_release_notes_draft.md`: the call-shape fix, the closed Python range, and the
  removal of the `ValidatedPayload` passport.
- `1.0.0_checklist.md`: final stability and interoperability gate for `1.0.0`.
- `1.0.0_release_notes_and_migration_summary.md`: release narrative and migration summary draft for final promotion.
- `1.0.0_go_no_go_pack.md`: final pre-tag evidence pack used for go/no-go decision.
- `notes_dev.md`: active engineering notes, recent decisions, and pending work.
- `smonitor.md`: diagnostics integration rules and non-negotiable SMonitor practices.
- `collective_evidence_pack.md`: cross-repo evidence handoff for collective 1.0 closure.

## Incoming work

- `pending_bugs/`: defects reported against a released version, one file each, written
  from the reporter's side — what happens, how to reproduce it, how it was found.
- `pending_proposals/`: designs proposed but not implemented, whether still open or
  already declined. A proposal leaves only by being implemented. A declined one stays,
  with a verdict header at the top naming the date, the reason, and what serves the case
  instead — the reasoning is the part worth keeping, because it is what stops the same
  design being proposed again, and it only does that where the proposals are read.
- `solved_bugs/`: reports whose defect has been fixed. A report is moved here rather
  than deleted, with a note at the top naming the commits, the tests that hold the fix,
  and anything a consumer has to do differently now. The report is the only place the
  *symptom* is written down, which is what makes the next similar defect recognisable.

## Maintenance rule

Keep this folder aligned with:
- `README.md` (public project framing),
- `docs/` (published user/developer documentation),
- `.github/workflows/` (actual quality gates and release behavior).
