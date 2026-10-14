---
summary: Register diagnostics without bootstrapping the application's policy.
issue: uibcdf/argdigest#32
status: partial
opened: 2026-10-13
closed:
severity: medium
verification: reproduced
area: [diagnostics, initialization, integration]
guard: tests/test_diagnostic_registration.py
normative:
blocked_by: []
supersedes: []
---

# Registration-only diagnostics

## Public-provider receiving — 2026-10-14

The external publication block is lifted: SMonitor 0.20.0 delivered the
capability and uibcdf/smonitor#48 and uibcdf/smonitor#50 are closed. Receiving now uses public
SMonitor 0.21.0 `py_2` and DepDigest 0.15.1 `py_0`. Their downloaded archives
match the release digests and their installed Python files match those archives.

A fresh Linux/Python 3.14.8 Conda environment installed a private ArgDigest
wheel built from `823146808b4af3203b8d3886c1d215b46b2c9f6f`. Outside the source
checkout, with PYTHONPATH unset, safe Python paths and importlib collection,
390 tests passed; one sibling-source collective test was unavailable in the
isolated parent. The required registration-only and scoped-capture cases ran;
`pip check` passed. After testing, 39 ArgDigest, 40 SMonitor and 17 DepDigest
Python files still matched their original wheel/public archives. Receipt:
`devguide/evidence/registration_only_receiving_2026-10-14.json`.

This is one installed private-wheel receiving check, not a new public ArgDigest
release or a complete platform/Conda-artifact qualification. Resume preparation
of the new exact ArgDigest release and its required gates. The existing 0.15.0
plan/artifacts and declared dependency floors remain unchanged. DepDigest's new
DeclaredRegistry features are not adopted by this compatibility check.

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

SMonitor owns bundle/direct emission and its console fallback. Provider
issue uibcdf/smonitor#48 delivered the per-bundle/per-call bootstrap_policy=False
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

The earlier source runs used a shared development environment with seven
unrelated conflicts tracked under uibcdf/molsyssuite#82. Those runs do not prove
a fresh installed closure. The separately created receiving environment above
passes pip check; it does not repair or modify that shared environment or prove
additional platforms/public ArgDigest delivery. No metadata floor, immutable
release plan/version or public artifact is changed.

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
