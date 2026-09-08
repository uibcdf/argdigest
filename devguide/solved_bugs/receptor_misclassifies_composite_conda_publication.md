---
summary: Use the release profile for action-internal Conda publication.
issue: uibcdf/argdigest#10
status: resolved
opened: 2026-09-08
closed: 2026-09-08
severity: low
verification: reproduced
area: [tooling, release]
guard: tests/test_gh_run_receptor_policy.py
normative:
blocked_by: []
supersedes: []
---

# The configured Conda matrix is not visible to GitHub

## What

ArgDigest requires four native platforms in its GH Run Receptor rule, but GitHub exposes
only Python-version jobs. The native platforms are inputs to
`uibcdf/action-build-and-upload-conda-packages@v2.0.1` and are built inside that action.
The receptor therefore cannot satisfy `expected_platforms` from GitHub job or artifact
identity. This is the topology that produced a false derived `FAIL` in
`uibcdf/smonitor#10`.

## How

Select `release` for the observable publication workflow and keep Anaconda as an
independent delivery gate. The release profile retains GitHub's status, conclusion, event,
SHA, ref, and visible steps without claiming hidden platform or registry results.
Structured producer support remains tracked in `uibcdf/gh-run-receptor#35`.

## Why

The current rule is valid syntax but asserts evidence GitHub never exposes. This creates
noise in the preferred first-inspection path and can train maintainers to ignore a future
genuine required-platform failure.

## What is measured and what is assumed

Source inspection confirms one Python matrix and four native-platform inputs inside the
shared publishing action. The equivalent SMonitor shape is measured in provider issue
`uibcdf/gh-run-receptor#35`; no ArgDigest release run is claimed as local runtime evidence.

## What was refuted

- Filenames, triggers, and action inputs do not prove visible platform completion.
- Removing only `expected_platforms` would hide the mismatch behind zero observed
  platforms.
- Selecting `release` does not prove Anaconda publication.

## Scope and exclusions

This change does not modify publishing, infer registry delivery, or implement the
provider-side structured matrix contract.

## Acceptance criteria

- The exact rule selects `release` without `expected_platforms`.
- GH Run Receptor 0.19.0 accepts and explains the rule.
- A local test guards the evidence boundary and the provider issue stays cross-linked.

## Dependencies and risks

The workaround is not blocked by `uibcdf/gh-run-receptor#35`; revisit it when that issue
provides reviewed structured producer evidence.

## Resolution

The exact workflow rule now selects `release` and no longer declares native platforms
that GitHub cannot observe. The test-first guard failed against the former configuration
and passes after the correction. GH Run Receptor 0.19.0 accepts the rule and explains the
exact match as `profile=release`; external registry verification remains independent.
