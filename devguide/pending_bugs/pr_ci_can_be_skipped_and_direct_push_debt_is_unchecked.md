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
the dispatch was diagnostic. Hosted PR and the first real nightly execution
remain to be observed. Keep the issue open until those outcomes and the
platform-claim review are recorded centrally.
