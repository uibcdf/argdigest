---
summary: Adopt the shared issue-backed developer-guide lifecycle.
issue: uibcdf/argdigest#6
status: resolved
opened: 2026-09-07
closed: 2026-09-07
verification: inspected
area: [governance, reporting]
guard: tests/test_reporting_protocol.py
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Adopt the shared issue-backed developer-guide lifecycle

## What

Bring ArgDigest's existing bug and proposal records under the common MolSysSuite
lifecycle while preserving useful historical analysis and established archive paths.

## How

Document local path mappings, add the common metadata template, generate queue and
archive indexes, add offline validation, give every current queued document an issue,
and archive entries whose prose already records a closed decision.

## Why

ArgDigest already retained resolved bugs, but its proposal queue mixed active, declined,
and out-of-scope work and most legacy records had no stable issue identity.

## Acceptance criteria

- All current queue entries have open owning issues and common metadata.
- Already decided proposals are archived with closed issues.
- New and migrated reports pass the offline lifecycle validator.
- Queue and archive indexes are generated and checked by the test suite.
- Contributor guidance routes developers to the local and central protocols.

## Resolution

ArgDigest now maps its existing archive layout to the shared lifecycle, validates all
current reports offline, generates queue and archive indexes, and retains three named
pre-adoption records without rewriting their history. Issues #7 and #8 carry the two
closed legacy proposal decisions; #9 is the one proposal that remains open.
