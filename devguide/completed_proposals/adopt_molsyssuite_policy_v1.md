---
summary: Adopt the shared MolSysSuite policy and Ruff gate.
issue: uibcdf/argdigest#4
status: resolved
opened: 2026-09-06
closed: 2026-09-07
verification: measured
area: [governance, tooling]
guard: .github/workflows/molsyssuite-policy.yml
normative: AGENTS.md
blocked_by: []
supersedes: []
---

# Adopt the shared MolSysSuite policy and Ruff gate

**Completed:** 2026-09-07 at `22ad5da`.  
**Suite rollout:** `uibcdf/molsyssuite#6`.

## Proposal

Route suite-wide concerns to the MolSysSuite repository and adopt its immutable
`policy-v1.1.0` caller. Keep ArgDigest's product tests, scientific validation contracts,
release process, and any stricter local checks under this repository's ownership.

Define the local Ruff baseline explicitly for Python 3.11 with `E4`, `E7`, `E9`, `F`, and
`I`; pin Ruff 0.16.5 in the existing Python 3.13 development environment; and establish
the lint and format baseline in a separate mechanical commit. Preserve the existing
exclusion of declined value-certification prototype code from maintained test and quality
surfaces.

## Evidence before implementation

- `requires-python` is the canonical `>=3.11,<3.14` range.
- CI covers Python 3.11, 3.12, and 3.13, and development already selects Python 3.13.
- Ruff 0.16.5 with the common isolated rules reports 81 findings: 66 import-order
  findings, ten unused imports, four bare exception handlers, and one unused variable.
- `ruff format --isolated --check .` reports 108 files requiring formatting.
- The local suite collects 222 passing tests; two CLI tests require a writable checkout
  and fail only under the read-only sibling-repository sandbox.

## Acceptance criteria

- Contributor guidance distinguishes suite-wide and repository-local ownership.
- The development environment pins Ruff 0.16.5 alongside Python 3.13.
- Local Ruff configuration includes the common baseline and does not inherit unrelated
  settings from a parent directory.
- Ruff lint and format checks pass without changing ArgDigest behavior.
- The complete test suite and the shared MolSysSuite workflow pass.

## Resolution evidence

Ruff 0.16.5 fixed 70 safe lint findings and reformatted 103 maintained files in a
dedicated mechanical commit. A clean-checkout import discrepancy led to an explicit
first-party package setting and exposed the central false positives fixed by
`uibcdf/molsyssuite#9` and `#10`. Ruff lint and format checks pass, all 222 tests pass,
and Sphinx builds with three pre-existing heading warnings. GitHub Actions policy run
`34062887147` and repository CI run `34062886826` both pass on `main`.
