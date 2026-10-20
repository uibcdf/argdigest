---
summary: Register diagnostics without bootstrapping the application's policy.
issue: uibcdf/argdigest#32
status: resolved
opened: 2026-10-13
closed: 2026-10-20
severity: medium
verification: reproduced
area: [diagnostics, initialization, integration]
guard: tests/test_diagnostic_registration.py
normative:
blocked_by: []
supersedes: []
---

# Registration-only diagnostics

## Pre-release review — 2026-10-14

The remaining implementation review strengthens the fresh-process contract:
repeated registration returns the same declaration receipt, application-owned
root/diagnostic handlers survive real emissions, ordinary explicit setup keeps
the application's policy, and only `use_provider_policy=True` applies the
provider's recommendations. An unsupported override refuses before setup.

The installed test profile still selected SMonitor 0.19.0 and lacked
`--require-registration-only`. A new subprocess guard reproduced the resulting
false success: an injected unavailable capability skipped its case and pytest
returned zero. The profile now selects public SMonitor 0.21.0 / DepDigest
0.15.1 and requires registration-only plus scoped capture. The guard now passes
only when that real profile refuses the unavailable capability with the expected
qualification diagnostic. Lower-bound minimal-core compatibility is unchanged.

A fresh installed private wheel passes 393 tests with one unavailable
sibling-source collective case. All eight registration cases execute, pip check
passes and installed Python bytes still match the original archives. Final
bounded evidence is `devguide/evidence/registration_only_final_review_2026-10-14.json`.
A separate clean NumPy-free installation of the same wheel with public SMonitor
0.16.0 / DepDigest 0.11.0 passes the extended minimal-core probe, including the
new registration-only refusal and existing restrictive refusal. Its pip check
and original provider-archive byte checks pass. This remains one platform.
At that checkpoint the source/profile work was ready for the next release. At that checkpoint this issue remained partial
until its separately qualified public release satisfies the final acceptance
criterion; it is not closed on the strength of a private one-platform wheel.

The subsequent board review finds no open PRs or queued bugs. The only other
open issue, uibcdf/argdigest#9, is explicitly scheduled after 1.0 and does not
block 0.16.0. The 0.16.0 version decision, exact-source/full installed/minimal-core
matrices, artifact and publication remain the release phase, not completed work.

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

## Public qualification and reconciliation — 2026-10-20

The release was published on 2026-10-14; the queued status had not been
reconciled. Independent review now binds original source
`2b9c9b289ae9b1d97d3bf04250f5c882feab3d41`, annotated numeric tag and stable
release to `noarch/argdigest-0.16.0-py_0.tar.bz2`, SHA-256
`e82d82680d79ae3d5df9917b1662d2855ed8485128943b72ddec87a5769a467d`.
The original source/full matrix, repository/publication policies, producer,
twelve full installed cells, twelve NumPy-free lower-bound cells and same-file
promotion passed their exact required native jobs and steps on attempt 1.

Producer `38567520662`, installed matrix `38568051160`, minimal-core matrix
`38568053243` and promotion `38572471948` retain separate identities. Receipt
ZIP digests, original producer and archive coordinate/digest were checked,
including the independent actual upload receipt (the build-only action's
`upload_not_requested` is not the subsequent staging upload). Public registry,
solver index and downloaded archive agree; 38 nongenerated Python runtime
files match the original candidate.

Independent central run `39469657236` at
`b199b7e1805ed054d924b00eac8d68793e07916d` installs the same public bytes on
Linux, macOS arm64 and Windows with Python 3.14 and executes the installed
console `--help` outside source. All three exact installation/command receipts
pass. This is explicitly a console smoke check; the original twelve-cell full
installed and core matrices supply the broader release evidence.

Documentation run `38572423608` passed its installed-wheel and Sphinx steps.
Archival run `38572426093` and independent public source-archive verification
confirm source-only Zenodo record `23369539`, version DOI
`10.5281/zenodo.23369539`, concept DOI `10.5281/zenodo.22892325`. The downloaded
541,645-byte ZIP matches its published checksum; all 330 source files match
the original tagged Git tree. Package files are not claimed as Zenodo contents.

Normalized immutable identities, native jobs/steps, artifact digests and public
receipts are retained in
`devguide/evidence/release_0_16_0_public_receiving_2026-10-20.json`. The existing
`tests/test_diagnostic_registration.py` guard exercises the repaired bootstrap
mechanism in fresh processes and makes unavailable mandatory capabilities fail
qualification; it is relevant to this resolution, beyond mere addressability.

No rebuild, substitution, retagging, new upload/promotion, historical release-title
edit or scientific rerun was performed during reconciliation. Consumer
receiving remains separately owned, including Recorda #24 and Praxis #10 under
uibcdf/molsyssuite#82 / uibcdf/moli#40; publication alone does not widen a
consumer's metadata. Shared provider receiving is reported to
uibcdf/molsyssuite#106 and publication coordination to uibcdf/molsyssuite#45.
