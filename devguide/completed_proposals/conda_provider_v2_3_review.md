---
summary: Adopt reviewed shared v2.3.0 publish and promotion callers.
issue: uibcdf/argdigest#45
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: inspected
area: [distribution, tooling]
guard: tests/test_noarch_conda_publication.py
normative:
blocked_by: []
supersedes: []
---

# Conda provider v2.3.0 source adoption

## What

Review under uibcdf/molsyssuite#87. Publish and promotion callers select the
reviewed MolSysSuite SDK commit 95f693be10c9205ab9b912cb53453710a207bf45,
not the external action SHA. That SDK uses provider v2.3.0 at
87c70b1443d5f22d738ee3ddf812bdbe0152f6c2 for build/exact-upload/promotion.

## How

Reviewed both workflow diffs, accepted inputs/outputs and the delivered operation
compatibility/evidence. Build stays host-only, upload false until inspected exact
bytes; staged/direct decisions, secret mapping and gates remain. Exact-upload
preserves coordinate absence/no-force/binding; promotion preserves typed labels,
installed qualification and independent public poststate. Withdrawal is excluded.

The SDK also contains later validation improvements: member recipe/resource and
dependency inspection pass through its public tools with our actual inputs.
Its 71 relevant noarch/release/native-profile contract tests pass in an isolated
immutable source copy. Local member route tests cover forwarding, source gate
sets, staging-only dispatch, no duplicate release build and the existing core
pre-promotion guard. Dependency inventory hashes are updated for the two edited
callers. Installed gate remains at 13a661e348275496a677a1bfe9650d68a03713a3;
policy/preflight/operator/archival pins retain their distinct reviewed revisions.

## Why

This accepts source routing without inventing a registry operation. No build,
new release/tag/upload/promotion, credential change or existing artifact mutation
is executed. A future normal candidate must qualify the SDK's actual installed
and publication route; current successful source/administrative checks do not
claim that real delivery. No scientific gate is weakened or suspended route enabled.
