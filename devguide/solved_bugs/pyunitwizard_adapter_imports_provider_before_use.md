---
summary: Defer the optional PyUnitWizard adapter import until pipeline execution.
issue: uibcdf/argdigest#22
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: reproduced
area: [dependencies, integration]
guard: tests/test_pyunitwizard_boundary.py
normative:
blocked_by: []
supersedes: []
---

# Optional PyUnitWizard adapter import boundary

## What

Importing `argdigest.contrib.pyunitwizard_support` eagerly imported PyUnitWizard
inside a module-level try. This was an explicitly requested adapter boundary,
not a demonstrated leak from importing the ArgDigest root. DepDigest 0.13.0's
expanded scanner exposes the source-level import under `uibcdf/depdigest#27`;
provider/consumer adoption is coordinated in `uibcdf/molsyssuite#95`.

## How

At ArgDigest `fc07dcf`, the Python 3.14 development environment reproduced one
finding with `python -m depdigest audit --src-root argdigest --soft-deps
beartype,pydantic,pyunitwizard --json` (exit 1, adapter line 13). The executed
editable provider source was DepDigest
`ba670098a5b773e7f1570adc47b890d063bd5627`; its installation metadata was older
than its source and is not evidence of a public artifact.

The adapter now probes availability without importing the provider, and loads it
in `_load_puw`, guarded by `@dep_digest("pyunitwizard")`, on first execution.
Pipeline factories remain usable without importing their optional provider.
Existing missing-provider catalog diagnostics and argument context are preserved;
transitive import failures propagate instead of being reclassified as absence.
The same audit then returns zero findings and exit 0, without an exemption.

## Why

Constructing a pipeline describes a contract; executing it needs the provider.
Keeping those stages separate removes the eager import while preserving the
adapter's value, unit and error behavior. No new provider capability or higher
runtime dependency floor is required.

## Acceptance criteria

- Importing the adapter and constructing factories do not import PyUnitWizard.
- Executing existing quantity operations retains their conversion semantics.
- Missing-provider diagnostics retain their catalog code and argument context.
- A provider's transitive import error remains distinguishable from absence.
- The expanded DepDigest audit passes without an exemption.

## Validation and guard

The 26 focused adapter, cross-layer and integration tests passed in Python 3.14.
`tests/test_pyunitwizard_boundary.py` guards the failure mechanism in an isolated
interpreter which refuses any PyUnitWizard import during adapter/factory setup.
The same module checks execution-time loading/reuse, catalog context, and the
identity of an injected transitive import exception. Existing installed-provider
tests verify conversions and canonical arrays. The complete Python 3.14 suite
passes (291 tests, three expected missing-digester warnings), Ruff lint/format
and generated indexes pass. Beartype 0.22.9 was added to the development
environment before the full-suite run; Conda also updated OpenSSL to 3.6.5.
HTML documentation builds in the repository's documented Python 3.13 docs
environment, with three existing heading warnings in `docs/index.md`.
Hosted qualification passed in [PR #23](https://github.com/uibcdf/argdigest/pull/23)
at source head `965cdf01b1952a22b080b939360ffff9a64dab83`:
[routine CI](https://github.com/uibcdf/argdigest/actions/runs/37201939802)
executed the Python 3.14 test job (290 passed, one skipped, three warnings),
wheel build/install and import from outside the checkout. The hosted environment
installed public DepDigest 0.13.0 and PyUnitWizard 0.27.0. The
[suite policy](https://github.com/uibcdf/argdigest/actions/runs/37201940155)
also passed. These are PR/source and wheel-smoke checks, not a new ArgDigest
release or its full installed compatibility matrix.

Canonical `DEPDIGEST_GUIDE.md` synchronization remains centrally owned; this
change does not edit a generated guide or claim adoption by another consumer.

## Resolution — 2026-10-04

The narrowed guarded import is implemented and tested without an audit exemption.
The addressable guard `tests/test_pyunitwizard_boundary.py` protects the exact
eager-import mechanism and preserves the absence/transitive-failure distinction.
Public-provider runtime evidence and the local expanded audit are recorded above.
Guide synchronization remains with the central `uibcdf/molsyssuite#95` owner.

## Guide delivery — 2026-10-04

The central owner delivered the expanded public DepDigest 0.13.0 guide in
ArgDigest `1790e4a7cb32bf3f621447396955877c73654dbd` while PR #23 was being
verified. The PR incorporates that upstream commit unchanged. The source audit
contract is now available in the synchronized copy; the earlier pending-guide
statement above records the state before this independent delivery.
