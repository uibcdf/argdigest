---
summary: Register diagnostics without bootstrapping the application's policy.
issue: uibcdf/argdigest#32
status: blocked
opened: 2026-10-13
closed:
severity: medium
verification: reproduced
area: [diagnostics, initialization, integration]
guard: tests/test_diagnostic_registration.py
normative:
blocked_by: [uibcdf/smonitor#48, uibcdf/smonitor#50]
supersedes: []
---

# Registration-only diagnostics

## Maintainer disposition — 2026-10-13

Diego explicitly authorized direct integration/push of the prepared provider
and consumer changes. Provider owner review is complete; the source changes
are accepted for main. SMonitor publication and the new exact ArgDigest
installed/release qualification remain pending. Source integration does not
make the capability available in the existing public packages.

Diego chose to hand SMonitor 0.20.0 publication to its maintainers and wait for
uibcdf/smonitor#50. ArgDigest release preparation is deferred until that
provider release is publicly available with its exact artifact and installed
qualification evidence. Then verify the published registration-only capability
and resume ArgDigest's own new-version qualification. An issue closure alone
does not replace the required public-package evidence.

## What

Recorda needs public ArgDigest declarations without implicit application setup.
The original 0.15.0 behavior changes unconfigured-manager config, warning hooks
and root handlers. Preconfigured applications are preserved; a capture scope
does not prevent bootstrap. Submodule imports still execute the root initializer.

## How

Expose register_diagnostics and configure_diagnostics. The root selects pure
registration only when the provider exposes the supported declaration-only
bundle capability. Older providers preserve their existing behavior and refuse
an explicit unsupported request. The CLI chooses application bootstrap itself.

SMonitor owns bundle/direct emission and its console fallback. Proposed provider
issue uibcdf/smonitor#48 adds the per-bundle/per-call bootstrap_policy=False
choice; ArgDigest delegates instead of copying warning replay, formatting or
deduplication. DiagnosticBundle, direct failure events and type-check fallback
all honor the choice. DepDigest's bootstrap-prone import is deferred until the
optional Beartype backend is actually used.

Fresh-process tests cover unconfigured/configured applications, public APIs,
pipeline execution, real warnings, no scientific imports, scoped capture and
explicit setup. The strict --require-registration-only gate cannot succeed by
skipping the feature. Local integrated source validation passed all 391 tests
on Python 3.14.7 with the proposed provider. The original provider has separate
compatibility evidence: 388 passed and three capability-specific skips on the
published 0.19.0 provider.

The shared development environment has seven unrelated conflicts tracked under
uibcdf/molsyssuite#82. Source origins were checked; these runs do not establish a
fresh installed dependency closure, more platforms or public delivery. No
metadata floor, immutable release plan/version or public artifact is changed.

## Why

A declaration-only import alone is insufficient: later bundle warnings and a
dependency import can re-enter setup. Ownership stays with SMonitor for shared
emission and with ArgDigest for consumer timing. Application policy remains
explicit, without environment-wide switches or private downstream patches.

## Acceptance criteria

- Owner review and qualified publication of the SMonitor capability.
- Public import/register/core execution/emission preserve both manager states.
- Existing providers and standalone CLI retain compatible behavior.
- Normal provider/shared notice in uibcdf/moli#62 before rollout.
- New exact ArgDigest release/installed qualification before Recorda adoption.
