---
summary: PR CI can be skipped and direct-push debt is unchecked
issue: uibcdf/argdigest#21
status: partial
opened: 2026-09-29
closed:
severity: high
verification: inspected
area: [ci, governance]
guard: tests/test_ci_backlog.py
normative:
blocked_by: []
supersedes: []
---

# PR CI can be skipped and direct-push debt is unchecked

**Detector correction on 2026-09-29:** the review in
`uibcdf/pyunitwizard#91` reproduced an old workflow-run listing from GitHub's
`branch=main` API filter, and the same behavior was observed in SMonitor.
This detector now lists runs without that API filter and checks
`head_branch=main` locally, together with commit ancestry and executed
Linux test steps. A focused regression rejects an otherwise green run from
a feature branch.

At `6223e01`, routine CI `36640865049` and policy `36640865725`
passed. The [corrected probe](https://github.com/uibcdf/argdigest/actions/runs/36640897094)
recognized `417ab9e` as the new executed full-matrix watermark and found
zero pending skipped commits; matrix jobs were omitted. The
[actual daily scheduled run](https://github.com/uibcdf/argdigest/actions/runs/36573874803)
had passed all twelve cells at `417ab9e`, including their test steps.
That run used the previous detector and reported no usable watermark plus
68 historical skipped commits, despite the earlier verified green manual
matrix. This is additional evidence for replacing the API branch filter.
The first real daily trigger is observed; hosted PR and platform-claim review
remain pending.

## What

At `ca537d2`, the primary `CI.yaml` PR test ignored documentation paths and
allowed `[skip ci]` in PR titles or `skip-ci` in branch names to skip its test
job. `main` had no effective branch rules. Direct-push skip markers had no
daily full-suite recovery. The
[weekly twelve-cell matrix](https://github.com/uibcdf/argdigest/actions/runs/36455538074)
passed at that exact commit, including executed `Run tests` steps in all four
Linux cells. This is a routing and enforcement gap, not a failed test suite.

## How

Run the complete Linux 3.13 PR test without workflow path or title/branch
skip conditions. Require its stable check on PRs, while administrators retain
direct pushes. Preserve the existing weekly and manual full matrix. Add a
conditional daily full matrix at 00:37 America/Mexico_City that detects
skipped commits since the last executed, green Linux matrix. If run history
or API evidence is unavailable, run it. A probe input checks the backlog
without dispatching test jobs.

## Why

ArgDigest is a shared support library. A green weekly matrix does not guard
a PR whose test job never ran, and repeated skipped direct pushes can leave
regressions unseen. The conditional daily route implements the suite policy
in `uibcdf/molsyssuite#39` without requiring a full matrix after each commit.

## Acceptance criteria

- The required PR test cannot be omitted by local filters or skip conditions.
- Skipped direct pushes stay due until an executed full Linux matrix passes.
- Hosted routine, full-matrix and probe evidence are recorded.
- Branch protection preserves direct pushes for the named internal maintainers.
- The first real nightly and PR route are observed before calling this adopted.

## Resolution

Commit `d1df25b` implements the workflow and detector. At that exact commit,
[routine CI](https://github.com/uibcdf/argdigest/actions/runs/36531091052)
and [MolSysSuite policy](https://github.com/uibcdf/argdigest/actions/runs/36531091809)
passed. The [probe-only dispatch](https://github.com/uibcdf/argdigest/actions/runs/36531106522)
recognized the executed weekly matrix `36455538074` at `ca537d2` as its
watermark, found zero later skipped commits, and omitted all matrix jobs.

The `main` branch now requires the strict `Test on ubuntu-latest, Python 3.13`
check. Administrators are exempt from the PR gate; the only current
collaborators with push permission are `dprada` and `LMMV`, both
administrators. The direct push of `8a34746` with `[skip ci]` exercised that
bypass. A [second probe-only dispatch](https://github.com/uibcdf/argdigest/actions/runs/36531382436)
found exactly that skipped commit after the `ca537d2` full-matrix watermark
and reported that full recovery is due. It omitted all matrix jobs because
the dispatch was diagnostic. GitHub did not show the new 00:37 scheduled run
during the observation window, so a
[manual full-matrix dispatch](https://github.com/uibcdf/argdigest/actions/runs/36532458998)
tested the current workflow at `9bb0a8e` and passed all twelve jobs,
including the four Linux `Run tests` steps. The
[post-matrix probe](https://github.com/uibcdf/argdigest/actions/runs/36532645259)
recognized `9bb0a8e` as the new executed watermark and found zero pending
skipped commits; its matrix jobs were omitted. Hosted PR and the first real
nightly execution remain to be observed. Keep the issue open until those
outcomes and the platform-claim review are recorded centrally.
