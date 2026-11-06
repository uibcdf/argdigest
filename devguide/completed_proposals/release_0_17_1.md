---
summary: Qualify and publish the 0.17.1 consumer-contract and diagnostics fixes.
issue: uibcdf/argdigest#51
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
area: [release, packaging, diagnostics, compatibility]
guard: tests/test_noarch_conda_publication.py
normative: devguide/conda_release_routes.md
blocked_by: []
supersedes: []
---

# Release 0.17.1

## Current outcome — 2026-11-05

0.17.1 is public in GitHub and Conda main, independently verified from a fresh
public installation, and archived as a source-only Zenodo snapshot. The exact
original file is retained from staging through main. Published guide/notes,
their executed source checks, rendered Pages deployment and owner handoffs
are verified separately. The dated preparation and operator observations below
retain their original scope. #9 and the separate CI-cancellation follow-up #52
remain deferred; consumer application receiving and guide distribution retain
their own owners.

## What

Diego explicitly authorized publication of 0.17.1 after reviewing #50. Include
the confirmed attribution repair, #43–#48 source corrections and #49's public
SMonitor 0.22.1 receiving/profile. MolSysSuite release-specific notice is #169;
thematic consumer/guide coordination remains #164. Original public 0.17.0 is
immutable and #9 remains deferred.

## How

Use the committed staged noarch build-0 decision. Retain exact-candidate fast
and twelve-cell source gates, build/inspection/original upload receipts, twelve
full installed cells with public scientific fixtures and nested-signal receiving,
and twelve separate NumPy-free lower-bound cells. Only then create immutable
tag/release 0.17.1 and promote the original tested file/digest to main.

Python 3.11–3.14, Linux/macOS arm64/Windows and required runtime floors remain.
Full installed SMonitor is 0.22.1, DepDigest 0.15.1 and PyUnitWizard 0.27.0;
the separate core matrix retains SMonitor 0.16.0 / DepDigest 0.11.0.
The optional PyUnitWizard API floor is corrected to >=0.22.0. Candidate/package
identity, native runs/attempts/jobs/steps and public/archival receipts will be
appended after each actually executed boundary. No candidate file is claimed yet.

Local #50 comparison fails seven of eight new controls on exact old source;
the fixed source passes all eight, 58 focused checks and the complete 528-test
selection with three known warnings, without skips. These are source checks,
not exact-file qualification. Subsequent candidate metadata/guidance and full
hosted/installed gates retain their own checks.

Pre-build review then found the #53 eager diagnostic-label lookup regression in
cb97df7. Six of fourteen expanded controls fail there; the corrected source
passes the complete 534-test selection, without skips and with the same three
warnings. The original candidate is superseded before any package build/upload.
The revised SHA must complete all gates; neither superseded matrix is a passed
release gate. #52 separately tracks ordinary workflow-cancellation behavior.

## Why

Users need published fixes for literal variadic keywords, native TypeError
catch families, optional checker failures and actionable consumer diagnostics.
Packaging/backend/publisher/profile changes justify staged exact-file receiving.
Consumer scientific acceptance and byte-identical guide distribution stay with
their registered owners; a provider release does not silently update clients.

## Executed qualification and publication — 2026-11-05

Original qualified source is `c9c9ee623dab5331fdfa4227bd784dd38620e18b`. Fast CI and policy checks passed;
source run `42071223440`, full installed `42111095969` and NumPy-free minimal core
`42111100594` each passed all twelve scientific cells and required executed steps.
Native identities, attempts, job sets and source/file/profile bindings were
independently verified before tag creation. The administrative source backlog
job was intentionally skipped; no scientific platform cell was waived.

Original producer `42094355330` created `argdigest-0.17.1-py_0.tar.bz2` (55,828 bytes), SHA-256
`5af09e12b0c3d344337f2a2d90ac8b5fcea5be8a8467694c41e3daac018c3899`. All 38 nongenerated runtime files match original candidate Git
blobs; the generated version and installed distribution are 0.17.1. SPDX MIT
metadata retains the original license notice byte for byte. Full qualification
uses public SMonitor 0.22.1 / DepDigest 0.15.1 / PyUnitWizard 0.27.0; the separate
core matrix retains public SMonitor 0.16.0 / DepDigest 0.11.0 and no NumPy.
Five additional Linux/Python 3.14 lower-bound probes of the real staged file
passed. They supplement the hosted matrices rather than replacing them.

The tagged GitHub Release title is exactly `0.17.1`, published at
`2026-11-05T23:08:36Z`. Same-file promotion `42127310186` passed its
release/core guard, original source/installed verification, main-label addition
and independent public index checks. Direct public download is byte-identical to
the original staged file. The clean public receiving prefix had no ArgDigest
before installation. Public CLI/provenance checks and the complete selected
scientific run passed: **533 passed, one absent-sibling E2E skip**, three known
warnings, all 28 SMonitor receiving controls passed. Runtime package bytes were
checked before/after; all provider imports remained in the public prefix and
`pip check` passed. This is additional Linux/Python 3.14 public receiving, not a
claim of consumer application acceptance.

Source-only Zenodo DOI `10.5281/zenodo.23991088` is independently verified. Its
691,522-byte ZIP, `md5:d21182b2640bcb754ec36325958d24b3`, matches all 362 files
of the original Git export byte for byte. No Conda-binary archival is claimed.
Release routing `42127303934` intentionally skipped another build for the staged
plan; release-event documentation `42127303380` and archival probe `42127303736`
passed. The maintained published guide and release-note update will receive
their own final documentation deployment and source/digest handoff.

## Operator corrections retained in the evidence

At context resumption, a task-local source monitor was duplicated. Both
controllers dispatched at the same source-gate completion. The second producer,
`42094355382`, built private digest
`e1b85da0dc946e4c737a71d1c29e8048d40a822ed907ea3598aa317c1bd13b68` and failed at
staging upload with an explicitly unverified receipt. The registry retained the
first producer's file. That failed duplicate qualifies no public artifact.
Actual native runs and receipts were reconciled, old controllers retired, and
exclusive task-local locks plus persistent pre-write markers protected subsequent
dispatch/publication. No producer was repeated during reconciliation and no
immutable coordinate or tag was overwritten. Native failed-step/receipt history
is retained separately in the qualification record.

The initial supplementary local scientific command also propagated
`PYTHONSAFEPATH=1` to trusted administrative child scripts, failing one report-index
test. The published workflow explicitly scopes `-P` to the scientific interpreter.
The same unchanged source/artifact passed with that documented invocation.
First/final XMLs, provenance records and the invocation correction are retained;
this was a local harness correction, not a skipped test or artifact rebuild.

The original queue diagnostic sampled only workflow runs marked `in_progress`
and missed active jobs in runs marked `queued`. Sampling was corrected and the
limited public-cohort observations, shared-plan capacity inference and original
qualification queue/cancellation history are retained without claiming a complete
private account/billing audit. No foreign run was modified or cancelled.

## Evidence and remaining ownership

`evidence/release_0_17_1_qualification_2026-11-05.json` binds the original producer,
all native gates, resource/runtime/license inspection and historical failed
attempts. `evidence/release_0_17_1_publication_2026-11-05.json` and the adjacent
receiving directory retain public file/index/installation and source archival
receipts. `tests/test_noarch_conda_publication.py` guards the route, immutable
coordinates, dependency/resource profile and wrappers; the concrete native runs
and public receiving above establish execution rather than static conformance.

MolSysSuite developers own all client guide-copy distribution under #164/#169,
retaining the maintainer's delegation in #125. Consumer developers own scientific
receiving and any workaround removal. This provider closeout edits no client
copy and claims no automatic consumer adoption.

## Administrative checkpoint — 2026-11-05

Publication receipts are retained while GitHub-hosted runners finish the
documentation closeout. Sphinx `42132020733`, suite policy `42131890739` and
publication policy `42131890803` passed at documentation source
`21f6ba42120d93467e3937ef2da0b54cd37e5d86`. Rendered gh-pages commit
`d149eff7d9bd577439a90fa107fb6bc112a1a2e9` contains the published 0.17.1 notes;
Pages run `42134555677` is still queued. The interim fast run retains its actual
state in the receipt; the latest evidence checkpoint receives applicable head
CI. None of these ordinary checkpoints replaces the fully executed original
C9 qualification. All three task-owned Conda prefixes and their private cache
were removed; the unchanged qualification branch was deleted with an exact-SHA
lease. The issue stays open until deployment, archival and final cleanup finish.

## Final documentation and ownership closeout — 2026-11-05

Canonical guide and published release notes are committed at `21f6ba42120d93467e3937ef2da0b54cd37e5d86`.
Guide SHA-256 is `1bb69c596cabd5d504416534ea952bea5fc7f23e74dea118cee47a4d196b965c`.
The exact revision/path/hash was delivered to MolSysSuite #169/#164 for all
registered client copies. Release-specific receiving notices were delivered
to ArgDigest #50/#53, PharmacophoreMT #82, DockingMT #19 and MolSysMT #428;
the retained handoff manifest links the actual comments. No client copy was
edited and no consumer scientific acceptance is inferred.

Documentation run `42132020733`, suite policy `42131890739` and
publication policy `42131890803` passed with required
jobs/steps executed at that source. Pages run `42134555677`
deployed rendered commit `d149eff7d9bd577439a90fa107fb6bc112a1a2e9` from that exact source;
its release-note HTML includes the published 0.17.1 text. Native deployment
and rendered content are verified independently of direct HTTP availability;
the receipt records any environment-limited HTTP observation separately.

The interim fast run `42131890287` retains its actual observed state in the
publication receipt. The final evidence commit receives its own applicable
latest-head CI/policy inspection, linked in the owning issue. This ordinary
checkpoint does not replace any original C9 release-qualification gate.

All three task-owned Conda receiving prefixes were removed through Conda.
The qualification branch was deleted only with a lease for original C9;
the immutable public tag and artifact remain. The task-local verification
SDK/venv/cache is retained only through the final evidence/checkpoint step.
The owning issue records final-head checks and completion of that cleanup.

## Upstream service observation

GitHub reported Actions/Pages degradation from 2026-11-05 23:36 UTC,
marked resolved at 2026-11-06 00:20 UTC in
<https://www.githubstatus.com/incidents/pfbmpxxfq1cy>. This overlaps the first
documentation queue; it does not establish an individual job cause. The af14bd1
checkpoint was requested after the published resolution. A later read-only
observer stopped on a TLS acquisition timeout and the next native read succeeded.
No artifact, build, promotion or deployment was repeated to repair that read.
The adjacent service observation preserves this limited scope.

A later recovery preflight also corrected an operator inference: the Pages
workflow was still queued, but its build had already passed and the status/deploy
jobs were queued. The preflight stopped before any cancellation or rerun request;
the original attempt was retained. The correction and no-write outcome are
recorded in `pages-queue-recovery.json`. Observers now preserve per-job states
without interpreting a queued workflow as entirely unstarted.
