---
summary: Classify missing optional Beartype without a required-library error.
issue: uibcdf/argdigest#46
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: reproduced
severity: medium
area: [diagnostics, optional-engines]
guard: tests/test_optional_typecheck_diagnostics.py
normative:
blocked_by: []
supersedes: []
---

# Optional type checking reported as required

## What

Real provider events show DEP-ERR-MISS-001/ERROR followed by an optional-engine
ARG warning while normal execution succeeds. Present but broken imports were
also silently converted into absence.

## How

Use public `depdigest.is_installed` at the feature boundary. Missing Beartype
returns no checker and emits one ARG-WARN-TYPECHECK-001 per affected decoration;
ordinary invocations emit no repeated absence notice. Separate decorated callers
remain observable rather than globally hidden. The required-dependency wrapper
is removed from this optional attempt, without suppressing any provider event.
A present engine's ImportError or missing transitive import propagates unchanged,
as do failures from checker construction. No new provider capability is needed.

Three fresh-process guards fail before the repair. Their real DepDigest/SMonitor
integration uses only controlled import finders for Beartype, no mocked
availability result. Two decorations work normally without importing Beartype,
produce exactly two ARG warnings and no DEP missing-required error. Broken and
transitive imports propagate; a genuine required dependency still emits its
original DEP error. Existing isolated emission-failure tests retain their focused
mocks, independently of these real-provider absence guards.

## Why

The consumer must not make Beartype mandatory or suppress diagnostics to correct
classification. Optionality and actual failures now have distinct observable
contracts; this source repair is not a new public package or consumer adoption.

## Isolated fallback-test ordering, 2026-11-05

Pre-build review under #51/#53 exposed two focused fallback mocks that depended
on DepDigest having been imported during earlier collection. Their availability
stub is now resolved before installing the artificial import failure, preserving
the intended optional-checker/emission assertions. Both tests pass when selected
alone. Real-provider fresh-process absence/broken/transitive guards are unchanged.
