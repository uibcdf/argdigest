---
summary: Prepare and qualify 0.17.0 with explicit contract ownership and alias/descriptor repairs.
issue: uibcdf/argdigest#40
status: resolved
opened: 2026-10-22
closed: 2026-10-22
verification: inspected
area: [release, contracts, distribution, integration]
guard: tests/test_contract_owner.py
normative:
blocked_by: []
supersedes: []
---

# Release 0.17.0

## Outcome

0.17.0 is public and independently verified. The annotated tag retains original
qualified producer `c7128f09b2fe064b6c5603d1077dbd2cec52223d`; promotion preserves
the same qualified file/digest. Public installation, documentation and source-only
Zenodo archival have separate receipts. Consumer adoption remains independently
owned under `uibcdf/molsyssuite#123`, and MolSysSuite developers own all client
guide-copy updates under `uibcdf/molsyssuite#125`. The dated sections below retain
preparation and qualification observations, followed by public closeout.

## What

The maintainer approved preparation on 2026-10-22 after the final review of
`uibcdf/argdigest#37`, #38 and #39. The additive public
`DigestConfig.contract_owner` API justifies 0.17.0. The scope includes canonical
supplied-name propagation and preserving staticmethod descriptors in both
decorator orders. The typing pilot under #9 is independent and nonblocking.

This issue owns preparation and subsequent qualification. No public release,
tag, artifact or consumer adoption is established by preparing these files.
Public publication remains a separate maintainer decision.

## How

Update the provider-owned canonical guide with the already public 0.16.0
registration-only diagnostics contract and clearly unreleased 0.17.0 ownership
guidance. Reconcile the stale 0.16.0 route text with its archived evidence.
Prepare release notes, citation metadata and a staged noarch build-0 plan.
Citation version/date are candidate metadata, not proof of publication; confirm
the actual release date before freezing the final publication candidate.

Retain Python 3.11–3.14 on Linux, macOS arm64 and Windows. Full installed tests
already select all `tests/`, including the 58 ownership cases and regression
guards. Keep public SMonitor 0.21.0 / DepDigest 0.15.1 and both mandatory
registration-only/scoped-capture switches. The separate core matrix retains
SMonitor 0.16.0 / DepDigest 0.11.0 and no NumPy. Extend its real runtime probe
with default/definition/exact ownership, inherited cross-module dispatch,
runtime display, staticmethod class/instance access in both orders and invalid
value refusal. No dependency floor or platform claim is widened.

Freeze an exact full candidate SHA after preparation. Verify fast CI, all twelve
source cells and applicable policy jobs actually execute. Build once through
the existing pinned shared producer; preserve source SHA, producer run/attempt,
filename, build number and sealed SHA-256. Qualify the identical installed bytes
in both twelve-cell matrices. Public tag/title `0.17.0`, exact-file promotion,
public registry/solver inspection, fresh public installation, docs and
source-only archival each require independent evidence after authorization.

## Why

The previous source suite passed 456 tests and exact-head fast CI, but those
results do not qualify a new installed artifact. Consumer-facing instructions
must distinguish released diagnostics from unreleased ownership and explain
logical lookup keys, fallback, runtime display and opt-in migration accurately.
`tests/test_contract_owner.py` guards the new selection and the two repaired
execution stages. The installed core probe checks their usable subset under
the retained dependency floors without borrowing the scientific environment.

## MolSysMT receiving scope

### Guide distribution ownership

The maintainer explicitly delegated all client `ARGDIGEST_GUIDE.md` updates to
MolSysSuite developers under `uibcdf/molsyssuite#125`. This preparation changes
only the ArgDigest-owned canonical source. Deliver its exact committed revision
and digest to #125; that owner uses the existing guide synchronizer for every
registered client and records destination commits/checks. Guide distribution
does not upgrade a package or qualify consumer behavior.

### Installed consumer behavior

Coordination remains in `uibcdf/molsyssuite#123`, linked to the resolved
motivating `uibcdf/molsysmt#404`. Before editing the consumer, select its actual
inherited native constructors and mixin entry points and compare current
behavior with the installed qualified provider:

- Preserve defaults, optional counts and successful canonical construction.
- Reject invalid counts and genuine unknown keywords with closed signatures.
- Verify the intended base/logical contract in inherited calls; preserve runtime
  child identity in diagnostics. Include independently decorated overrides and
  mixins that deliberately retain runtime ownership rather than assuming all
  inheritance should use definition mode.
- Exercise relevant aliases, function/domain rules and standardizer selection;
  ensure other caller-dependent digesters retain their current semantics.
- Keep `native_constructor` until the consumer demonstrates that the selected
  ownership option replaces its exact purpose. Do not remove it solely because
  the provider now offers another caller selection mechanism.

Record the exact provider file/digest, consumer commit, dependency closure,
executed tests and any retained exception. Provider qualification, consumer
source adaptation and public consumer receiving remain separate claims.

## Acceptance criteria

- Guide, route, notes and candidate metadata agree on release boundaries.
- The minimal-core probe exercises the new option without scientific dependencies.
- Preparation checks pass and the pushed head has inspected applicable CI.
- One exact candidate passes all source/policy gates and both installed matrices.
- Public publication is authorized and independently checked before claiming it.
- Consumer handoff states test scope, unknowns and workaround removal conditions.
- At release closure, archive this record, regenerate indexes and reconcile #40.

## Preparation validation — 2026-10-22

The 94 selected ownership, core/release-gate, noarch-publication and reporting
tests passed on Python 3.14.7 through `python -m pytest --receptor=llm`.
Ruff checks passed and all 282 Python files were already formatted. Generated
indexes and `git diff --check` passed. The existing shared
`conda_release_contract.py` accepted the 0.17.0 plan and publication callers;
that is administrative evidence only.

A disposable Conda environment installed public SMonitor 0.16.0 build `py_1`
and DepDigest 0.11.0 build `py_2`, Python 3.14.9, pip and their solver dependencies.
It installed a locally built development wheel without dependencies and ran
the extended `core_runtime_probe.py` outside the checkout with `python -P`.
All assertions passed, including the no-NumPy precondition and final import
check. `pip check` found no broken requirements in that isolated environment.
This is local probe validation, not the exact 0.17.0 Conda candidate or its
twelve-cell installed qualification. The development wheel was
`argdigest-0.16.0+8.gba8f20a.dirty-py3-none-any.whl`, SHA-256
`832740ada257d5708fa4001bb637653b2dc37e711a0a9888c805bc37cb07bc91`;
its VCS development identity must not be confused with a public 0.17.0 file.

The shared editable development environment still reports its seven unrelated
pre-existing dependency conflicts tracked under `uibcdf/molsyssuite#82`.
No shared environment was changed, and its tests are not a public closure claim.
The temporary wheel/environment/cache may be retired after this evidence and
the pushed preparation handoff are retained.

## Exact staged qualification — 2026-10-22

The maintainer authorized proceeding with qualification after preparation.
Original producer candidate is
`c7128f09b2fe064b6c5603d1077dbd2cec52223d`. Full source run `39878899217`
passed all twelve declared cells; fast CI `39878177354`, repository policy
`39878177580` and publication policy `39878177730` passed at that same SHA.
The existing shared native-gate verifier independently confirmed each required
job and test/check step executed on attempt 1. The source matrix's administrative
backlog job is intentionally inapplicable to this manual full run.

Producer `39879184044`, attempt 1, built once and uploaded only to staging:
`noarch/argdigest-0.17.0-py_0.tar.bz2`, SHA-256
`9c35fa297b5a85dc65ac49ccd108f60f08dbeac4f745d6c369a767c0a0b3a3e1`.
The shared `noarch_release.prepare_handoff` operation independently bound the
native producer steps, digest-verified receipt ZIP, archive inspection and
actual staging-upload receipt to this original candidate/file. Its verified
arguments were used for the full installed caller. This is actual operator
use; no active human-effort reduction was measured or claimed.

A separate download of the 55,325-byte archive matches the sealed digest.
The shared archive inspector checked noarch identity, generated version,
distribution metadata, dependency constraints and all nine declared resources.
All 38 nongenerated Python runtime files also match the original candidate's
Git blobs. Neither a rebuild nor substitution was performed.

Full installed run `39879578589`, attempt 1, passed preparation and all twelve
cells. All four required steps executed in every cell: exact-file installation,
installed-file validation, the complete selected tests and the final provenance
recheck. The source/file/profile binding receipt was independently acquired and
digest-verified. Core run `39879578248`, attempt 1, passed all twelve separate
cells with the retained public provider floors; its exact-byte/CLI checks and
extended NumPy-free runtime probe executed in every cell. Both native matrices
were independently verified against their exact source, workflow, title/digest,
attempt, job sets and required successful steps.

Native logs for all twelve source and twelve full installed cells each report
455 passed and one skipped. The only omitted case is
`tests/e2e/test_collective_error_path.py::test_collective_error_path_emits_contract_signal_and_dependency_hints`:
it explicitly prepends sibling source clones that hosted environments do not
contain. This does not stand in for consumer receiving. No ownership,
registration-only or scoped-capture case was omitted; the installed profile
requires both provider capabilities and fails if unavailable. The three
existing missing-digester warning groups remain visible.

Normalized native proofs, receipt/archive identities, per-cell counts/log
digests, binding, current registry labels and the concrete publication handoff
are retained in
`devguide/evidence/release_0_17_0_qualification_2026-10-22.json`.
The file remains under `staging` only. No remote tag, GitHub Release, main-label
promotion, public installation, new archival record or consumer adoption is
claimed. This report and #40 stay active until separately authorized publication
and its independent public/archival checks finish. Any later tag must target
the original qualified producer candidate, not an evidence-only successor.

### Administrative profile follow-up

The current central `argdigest-core-v2` profile was reviewed for 0.15.0 and
deliberately rejects this changed probe hash. An additive current-profile
review is requested in
[uibcdf/molsyssuite#92](https://github.com/uibcdf/molsyssuite/issues/92#issuecomment-6354595761);
the historical profile is not
relaxed or overwritten. The existing component route remains applicable:
shared producer/full installed qualification, independently verified core matrix
and unchanged `verify_core_release.py` before any promotion. This follow-up
does not block qualification or authorize publication. Guide distribution
continues to belong to MolSysSuite developers under `uibcdf/molsyssuite#125`.

Task-owned archive, native logs and receipts are retained at
`/tmp/argdigest-017-qualification.7E0JA0` for the publication/public-byte comparison,
with review on 2026-10-29 and removal after durable release closeout. Shared
clones, environments and unrelated resources are preserved.

## Public publication and closeout — 2026-10-22

After inspecting the qualified candidate, the maintainer explicitly authorized
the tag/release and exact-file promotion. The authorization is retained in
[uibcdf/argdigest#40](https://github.com/uibcdf/argdigest/issues/40#issuecomment-6354757849).
The original producer plan/tag source is unchanged; main's maintained plan and
guides now record the delivered state.

The stable GitHub Release is titled exactly `0.17.0`, matching its annotated tag
and public package version. It was published at `2026-10-23T00:55:50Z`, still
2026-10-22 in America/Mexico_City, matching the candidate citation date.
The tag points to the original qualified producer, not an evidence/docs successor.
The release event `39881034913` executed its source/tag/dependency decision and
intentionally skipped the build/upload job for the staged route.

Promotion `39881036506`, attempt 1, executed the existing public-release/core
guard, reacquired source and installed gates, added `main` to the same tested
file and independently checked registry/index state. Its receipt ZIP digest and
verified `staging` → `main` receipt are retained separately from the producer.
No rebuild, overwrite, retag or promotion retry occurred. Independent public
metadata/index verification and a downloaded 55,325-byte public archive match
SHA-256 `9c35fa297b5a85dc65ac49ccd108f60f08dbeac4f745d6c369a767c0a0b3a3e1`
and the earlier staging download byte-for-byte.

A disposable Linux Python 3.14.9 environment received that exact public archive
through the existing shared console receiver, outside both source checkouts.
Distribution/import versions, Conda URL/digest, launcher/module origins and
`argdigest --help` passed. A focused public runtime smoke also exercised
definition ownership, explicit pipelines and registration-only diagnostics,
without importing NumPy. This normal public solve selected SMonitor 0.22.0 and
DepDigest 0.15.1. Its CLI/focused smoke does not replace or widen the twelve-cell
full installed qualification with SMonitor 0.21.0, nor the separately qualified
lower-bound core matrix. Descriptor-permission notices from the restricted
local sandbox disappeared when the same focused smoke ran outside that sandbox.

Release documentation run `39881034395` passed its build/install/import and
Sphinx/deployment steps. The post-publication guide/release-note refresh at
`5d88ed18dda05d66d56ce4d6673275e7fd65c96d` passed docs run `39881672175`, fast CI
`39881607800` and both policies. Independent HTTP reads of the public
configuration and release-note pages confirm delivered 0.17.0 text and no
unreleased heading. The canonical guide's exact revision and SHA-256
`6e2137129995545492b57c09809f0e83d3f74d6f162260ecf79678f1f6f3b9a2`
were handed off to MolSysSuite developers in
[uibcdf/molsyssuite#125](https://github.com/uibcdf/molsyssuite/issues/125#issuecomment-6354864482).
No client copy was edited here.

Archival run `39881034787` independently reports public Zenodo record `23583152`,
version DOI `10.5281/zenodo.23583152`, concept DOI
`10.5281/zenodo.22892325`, open software and source-snapshot coverage. A separate
anonymous record query and download verified the single 594,818-byte
`uibcdf/argdigest-0.17.0.zip`, its published MD5 checksum and SHA-256, and all
338 tracked files against the original tagged Git tree. This archives source
only; it does not claim that the Conda package was deposited in Zenodo.

Complete normalized public identities, native step proofs, promotion receipt,
public registry/index/download, fresh installation scope, published pages and
source-archive verification are retained in
`devguide/evidence/release_0_17_0_publication_2026-10-22.json`, alongside the
original qualification evidence. The ownership/alias/descriptor assertions in
`tests/test_contract_owner.py` remain the relevant runtime guard for this release;
native and external receipts establish its distribution/publication boundaries.
The report is archived and indexes regenerated with this closeout. #40 closes
after its final evidence head checks and owner handoffs. The separate typing
pilot under #9, central profile review under `uibcdf/molsyssuite#92`, guide
distribution under `uibcdf/molsyssuite#125` and consumer receiving under
`uibcdf/molsyssuite#123` are not claimed complete.

All task-owned temporary environments, archives, logs and receipts can now be
retired once this durable closeout and issue handoffs are retained. The final
issue comment records actual cleanup; shared environments and clones stay intact.
