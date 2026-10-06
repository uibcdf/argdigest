# Contributing Workflow

This page defines the practical workflow for contributing to ArgDigest.

## Branching

- Create focused branches per feature/fix.
- Keep commits small and logically scoped.
- Avoid mixing refactors with behavior changes.

## Pull request expectations

- Explain behavior change and rationale.
- Reference updated docs when public behavior changes.
- Include tests for new behavior or regression prevention.

## Required checks before merge

1. Test suite passes.
2. Documentation stays aligned with code behavior.
3. Public API impact is explicitly stated.

## Documentation contract

Any change touching integration behavior must update the relevant pages in:
- `docs/content/user/`
- `docs/content/developer/` (if contributor workflows or internals changed)
