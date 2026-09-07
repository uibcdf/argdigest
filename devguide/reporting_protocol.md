# Reporting protocol

This repository implements the common lifecycle accepted in `uibcdf/molsyssuite#11`.
That central policy owns the shared meanings; this document maps them to ArgDigest.

## Ownership and identity

ArgDigest-specific bugs and proposals use `uibcdf/argdigest#<number>`. Suite-wide
policies, tooling and cross-repository decisions use `uibcdf/molsyssuite`. Cross-repo
references always use `uibcdf/<repo>#<number>`.

Every queued document must have an owning issue. Not every incoming issue needs a
document: create one after triage when the theme needs durable analysis.

## Local paths

- `pending_bugs/`: open defects;
- `pending_proposals/`: open proposals;
- `solved_bugs/`: resolved defects;
- `completed_proposals/`: implemented proposals;
- `archive/withdrawn_proposals/`: withdrawn or superseded proposals.

These three resolved locations together are ArgDigest's permanent archive. Historical
files listed by `devtools/devguide_reports.py::LEGACY_ARCHIVE` predate adoption and remain
immutable without retrofitted issue metadata. No queued report is exempt.

## Filing and closing

Open the issue first, copy `templates/report.md`, fill the common metadata, expand the
What / How / Why analysis, and regenerate indexes. At closure, set a closed status and
date, cite a test in `guard` or a durable rule in `normative` for resolved work, move the
record to its mapped archive, regenerate indexes, and close the issue with the outcome,
guard, and final record path.

**Archive, never delete.** Correct open reports in place. Append a dated correction to
an archived report rather than rewriting the original historical claim.

GitHub issue state and report state must agree after filing and closing. Network board
operations remain manual; the repository guard is deliberately offline.

## Checks

```bash
python devtools/devguide_index.py
python devtools/devguide_index.py --check
python -m pytest -q tests/test_reporting_protocol.py
```
