# Migration: warn to error

This page defines a practical path from permissive to strict digestion.

## Stage 1: `strictness="warn"`

Goal:
- discover missing digesters without blocking users.

Actions:
1. collect warnings in tests and CI logs,
2. prioritize high-frequency arguments,
3. remove inline legacy checks while adding digesters.

At this stage, the objective is observability rather than enforcement. You want
to see where digestion coverage is missing while keeping functional behavior
stable for users.

## Stage 2: warning budget

Goal:
- establish measurable progress.

Actions:
1. define a warning baseline,
2. require "no new missing-digester warnings" in CI,
3. reduce baseline until it reaches zero on migrated modules.

The warning budget is what turns migration into an engineering process instead
of an open-ended cleanup effort. It gives the team a concrete signal of
progress and prevents regression by default.

## Stage 3: `strictness="error"`

Goal:
- make missing digester coverage an enforced contract.

Actions:
1. switch mature modules to `error`,
2. keep transitional modules in `warn` only if explicitly justified,
3. remove transitional justifications after coverage completion.

By the time modules move to `error`, missing digesters should be treated as
integration defects, not as acceptable runtime variation.

## Done criteria

- no unexplained missing-digester warnings in CI,
- API entry points run with strict digestion enabled,
- migration notes are updated for contributors.

These criteria are intentionally strict: they confirm both technical coverage
and team-level maintainability.

## Next

Continue with [Integrating Your Library](integrating-your-library.md).
