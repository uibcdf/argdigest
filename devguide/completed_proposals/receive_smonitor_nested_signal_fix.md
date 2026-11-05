---
summary: Receive the accepted SMonitor nested-signal observation correction.
issue: uibcdf/argdigest#49
status: resolved
opened: 2026-11-04
closed: 2026-11-05
verification: measured
area: [diagnostics, integration, receiving]
guard: devtools/tests/receive_smonitor_nested_signals.py
normative:
blocked_by: []
supersedes: []
---

# Receive nested-signal correction

## What

SMonitor has accepted the filtered-inner-DEBUG correction and its reentrant
callback follow-up in `uibcdf/smonitor#59` and `uibcdf/smonitor#61`. The exact
accepted main is `ccdcace55ba5caf431b4a6a6904d8d18173114a3`. Suite coordination
is `uibcdf/molsyssuite#163`; the requesting consumer is `uibcdf/dockingmt#19`.
ArgDigest's source/private-wheel reception and subsequent public-file reception
pass. Public SMonitor 0.22.1 is selected by the development full installed profile;
the general runtime minimum and separate minimal-core profile remain unchanged.

## How

Keep ArgDigest's normal signal composition. Do not reorder consumer decorators,
clear private flags, copy provider logic, raise production verbosity or update
diagnostic baselines automatically. Once the owner provides an accepted exact
provider/public file, compare filtered DEBUG, accepted DEBUG, nested ERROR,
disabled/silenced diagnostics, catalog/native exceptions, configuration and
restrictive capture. Preserve exception identity, args and causes.

### Initial control before owner acceptance

A bounded source control on the actual editable SMonitor visible in the shared
environment already observes outer ERROR at WARNING threshold and DEBUG at
DEBUG threshold, with the same ValueError object/args/cause in both cases.
This is a positive source-composition control, not a reproduction of the old
provider failure and not a public receiving claim. ArgDigest source is 7fdf726.
The provider HEAD observed for that invocation was
`82dad5a7e26e0fba712e30657a6739188d770d79`; a concurrent owner commit then advanced
it to `7fad8f5` with additional tests. The runtime file hashes captured are:

- `smonitor/core/decorator.py`:
  `04bbc6b5b9e37c5ec98975ea868f70c4aa2a258d3f747afa8a2c6c72a97f22ab`;
- `smonitor/core/manager.py`:
  `bc7ae0cd5e01f4e075483edadd474ac3b9f782d20cf71e333de1f11c38c1e71a`.

The shared clone and environment were not changed by this control. The owner's
original baseline/private-wheel comparisons remain in the linked provider issue.
At that checkpoint this report stayed blocked for the accepted-provider/public
receiving decision; the local source control was not completed public adoption.

### Accepted-source reception, 2026-11-04

Private wheels built from isolated exact exports compare accepted SMonitor
`ccdcace55ba5caf431b4a6a6904d8d18173114a3` against the pre-fix baseline
`a3fd6d9858973b887e7a8ef0ed1b44f1dd1f2a1d`, using ArgDigest
`7e09e974c36bcf5cace99a7b898d0f5f7a9d3ff2` in both environments. All 40 provider
runtime Python files and 38 ArgDigest runtime Python files match their exact
source; generated version files are excluded from source equality. These archive
builds have versioningit fallback metadata `0.0.0+unknown`, not public versions.
Wheel SHA-256 values and installed-file hashes are retained in
[`smonitor49_source_receiving_20261104.json`](../evidence/smonitor49_source_receiving_20261104.json).

On Linux Python 3.14.7, the new explicit receiving module passes **28 controls**
against the accepted wheel, with no skips or warnings. The identical module
fails **10 controls** against the old provider (18 pass), specifically missing
actual ERROR observations after filtered/silenced inner signals and call-shape
rejection. This adverse comparison protects the reported mechanism rather than
asserting private marker shape.

Controls cover native/catalog exceptions, WARNING/DEBUG/CRITICAL thresholds,
disabled diagnostics, inner-source silence, repeated outer ERROR wrappers,
identity/args/cause, original catalog code/context and zero payload conversions
under restrictive capture. Pipeline and unknown-argument rejection exercise
validation before the function body. At DEBUG, the pipeline's own ERROR signal
and its separate DEBUG catalog diagnostic both survive; these are distinct
observations, not duplicate exception signals. Application configuration identity
and active capture policy remain unchanged during the operations.

The existing related selection passes **57 tests**. The full exported ArgDigest
`tests/` selection passes **491 tests**, with **one existing collective E2E skip**
because sibling repositories are absent in the isolated export, and three known
missing-digester warnings. This is bounded Linux integration evidence, not the
full public twelve-cell matrix or collective sibling E2E acceptance. Actual
ArgDigest/SMonitor/Pytest Receptor import origins are installed in temporary
environments outside the checkouts. Published Pytest Receptor 1.2.2 supplies the
test rendering; supporting dependencies inherit the shared environment, including
editable DepDigest/PyUnitWizard, whose post-run snapshot is recorded explicitly.

The receiving module is selected explicitly as documented in
[`devtools/README.md`](../../devtools/README.md#explicit-smonitor-nested-signal-receiving).
Its `receive_` filename avoids making this unreleased provider correction an
implicit requirement of existing historical/core/full installed profiles. It
contains no skips, version detection, baseline updates or provider workaround.

### Public receiving pending at the source checkpoint

The latest public GitHub Release at this checkpoint is SMonitor 0.22.0, predating
the correction. Diego reports that the owners are preparing a new publication.
Once available, receive the exact channel/build/file/digest, verify installed
origins, rerun the explicit controls and relevant existing tests, then record the
public profile and capability-floor decision. Keep #49 open until this evidence
and decision exist; provider source closure alone does not complete adoption.

### Public 0.22.1 receiving and resolution, 2026-11-05

SMonitor 0.22.1 is public under `uibcdf/smonitor#62`, with immutable tag/source
`2147c7c641b7cba8a974b193207f686ee3ebe855`. The downloaded main-channel file
`smonitor-0.22.1-py_0.tar.bz2` is 60,043 bytes with SHA-256
`e9ce6c77a682dddec3a6e724f9cc98cca31c4d6732453d554107ffcf61f23e7e`.
The registry and both actual Conda records agree with that identity. All 42
provider payload files match the downloaded archive before and after tests.

Two isolated Linux x86_64 Python **3.14.10** prefixes use public UIBCDF and
conda-forge packages with strict priority, without system-site-packages or
editable sibling dependencies. One installs a private ArgDigest wheel from exact
source `a463a9eaceb0661c1a111a8883962282ce1ed169` (38 runtime Python files
verified; archive fallback version `0.0.0+unknown`). The other installs public
ArgDigest **0.17.0**, original file `argdigest-0.17.0-py_0.tar.bz2`, SHA-256
`9c35fa297b5a85dc65ac49ccd108f60f08dbeac4f745d6c369a767c0a0b3a3e1`.
Both use public DepDigest 0.15.1 and PyUnitWizard 0.27.0. `pip check` passes in
both. Runtime origins remain installed before and after scientific tests; no
shared clone or environment is modified.

| Selection | Current ArgDigest runtime | Public ArgDigest 0.17.0 |
| --- | --- | --- |
| Explicit receiving controls | 28 passed | 28 passed |
| Complete selected installed suite | 519 passed, 1 skipped | 455 passed, 1 skipped |

The current full selection includes the 28 receiving controls; the released
suite retains its original selection, with its receiving controls run separately.
Both skips are the existing sibling-clone collective E2E, absent from these
isolated exports. The shared installed runner produces two pre-import assertion
rewrite warnings; full suites also retain three known missing-digester warnings.
No diagnostic or warning baseline is changed. The exact provider's own 47
signal/filter/callback regression controls also pass on its public installed
artifact, without skips or warnings. Public command/archive checks verify both
packages' resources, versions, Conda records and installed `--help` commands.

The revised receiving guard names `UnknownArgumentError` for catalog call-shape
rejection, so this provider gate is independent of the separate unreleased #48
TypeError-inheritance correction. Its outcome and payload checks remain active
on both ArgDigest generations. The prior adverse source comparison above retains
its original module hash and is not claimed as a rerun against this revision.

Full source/package/environment/provenance/results are in the
[public receiving receipt](../evidence/smonitor_0_22_1_receiving_20261105/receipt.json),
with the frozen executed wrapper around MolSysSuite's existing installed runner.
That runner already supports multiple selected paths. The separate public-file
command verifier is used for main-channel records; a staging-only verifier is
not treated as public-file acceptance. Recipe/resource and dependency-route
preflights pass.

### Accepted profile and capability decision

`devtools/conda-build/resources.toml` now selects `smonitor==0.22.1` and both
`tests/` and `devtools/tests/receive_smonitor_nested_signals.py` for future full
installed candidate matrices. The guard has no version probes or skips: it
asserts actual handler/history observations, first-admitted deduplication and
native/configuration/capture preservation. These assertions cover #49's failure
mechanism and remain mandatory in the selected profile.

The general `smonitor>=0.16.0` declaration and separate minimal-core profile
retain compatibility with historical providers. The canonical ArgDigest guide
documents **SMonitor >=0.22.1** as the capability floor for the corrected nested
observation guarantee, and does not promise it on earlier providers. Distribution
of the canonical guide and central test-edge registry updates remain with
MolSysSuite's owners, via the existing coordinated handoffs.

This closes ArgDigest #49's owner receiving and profile decision. It does not
claim a new ArgDigest release or a new twelve-cell client-pair qualification.
Only Linux/Python 3.14.10 was executed here; future ArgDigest candidates retain
their complete source/full-installed/core/public gates. Provider twelve-cell
qualification belongs to SMonitor #62 and cannot substitute for client gates.

## Why

Additional outer diagnostic observations can change QA identities/counts without
changing native failures. The provider must own acceptance/publication; ArgDigest
owns its subsequent receiving tests and dependency/guide decisions. The follow-up
is independent of the completed #43–#48 source repairs and the #9 typing deferral.
