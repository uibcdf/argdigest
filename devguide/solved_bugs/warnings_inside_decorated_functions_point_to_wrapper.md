---
summary: Warnings inside decorated functions point to the ArgDigest wrapper.
issue: uibcdf/argdigest#16
status: resolved
opened: 2026-09-24
closed: 2026-09-26
severity: medium
verification: inspected
area: [documentation, warnings]
guard:
normative: standards/ARGDIGEST_GUIDE.md
blocked_by: []
supersedes: []
---

# Warnings inside decorated functions point to the wrapper

## What

`warnings.warn(..., stacklevel=2)` inside a function decorated with `@arg_digest`
can report `argdigest/core/decorator.py` as its source. Sabueso observed this with a
function also decorated by SMonitor; see `uibcdf/smonitor#23` for that layer.

## How

The normal ArgDigest call path includes `_invoke`, `_run_digestion`, and `wrapper`
between the decorated function and its caller. The warning emitter chooses its own
`stacklevel`; a decorator cannot change an existing `warnings.warn` call's argument
without replacing the warning machinery. The canonical guide now names the current
frames, states that their count is not stable, and explains the Python 3.12+
`skip_file_prefixes` and Python 3.11 dynamic-stack approaches for consumers that need
call-site attribution.

## Why

A fixed hand-counted level works only for one wrapper arrangement. Adding ArgDigest or
another decorator silently invalidates it, as the Sabueso case showed.

## Evidence and limits

The issue's Python 3.13 frame trace at `uibcdf/sabueso@4b4c153` shows the three
ArgDigest frames followed by SMonitor frames. Source inspection on 2026-09-26 confirms
those ArgDigest frames are still present. This resolution documents the contract and
consumer remedies; it does not rewrite warnings emitted by consumer code.

## Acceptance criteria

- The guide explains why a fixed `stacklevel` may name the wrapper.
- The guide gives a version-aware remedy and does not promise a stable frame count.
- The cross-library SMonitor issue remains independently owned.
