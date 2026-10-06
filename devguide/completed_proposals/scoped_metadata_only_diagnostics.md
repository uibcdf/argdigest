---
summary: Apply SMonitor capture policy before ArgDigest-owned diagnostic collection.
issue: uibcdf/argdigest#29
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: measured
area: [diagnostics, integration]
guard: tests/test_capture_policy.py
normative:
blocked_by: []
supersedes: []
---

# Scoped metadata-only diagnostics

## What

ArgDigest converts native failures to text and formats rule/value diagnostics
before SMonitor can filter them. Recorda's proposed configuration integration
requires preventing those conversions, not only removing retained output.

## How

Consume SMonitor's public CapturePolicy, diagnostic_scope and get_capture_policy
from source commit 6feac9728cc35d57cbc92f284d7040d7f04cb35b. The last observed
published release is 0.18.0 and lacks this API. Preserve detailed behavior on
the existing provider floor; explicitly requested restrictive capture must fail
closed when the capability is unavailable. Source qualification is separate
from public provider publication and Recorda receiving qualification.

## Why

Capture policy belongs to SMonitor. ArgDigest owns its pre-emission conversion,
validation contexts, adapters and fallback precedence. No independent global
policy engine or Recorda dependency is needed.

## Acceptance criteria

- No automatic arbitrary repr/native str on restricted success or failure.
- Known catalog events and bounded public identity; no value/context payloads.
- Native identity/cause/traceback and existing adapter translations preserved.
- Contracts, digesters, normalization, pipelines and profiling still execute.
- Nested/concurrent policies compose through SMonitor and restore on exit.
- Diagnostic fallbacks preserve the operation outcome; rich defaults remain.
- Document capability availability and validate source and old-provider paths.

## Local implementation

`capture_policy` is accepted by the decorator/map alias, DigestConfig, module and
file loaders. The implementation delegates nesting/concurrency to SMonitor and
checks current permissions before rendering details or native failures. Runtime
contexts remain unchanged; telemetry excludes their value/all_args. Explicit
failure events now use ArgDigest-owned catalog codes rather than the borrowed
MSM debug code. Fixed fallback warnings preserve failure precedence. Rule
execution no longer calls str(rule) merely to prepare a diagnostic label.

`tests/test_capture_policy.py` checks repr/str counters, both failure paths,
contracts, alias collision, runtime context, profiling, nesting, tasks/threads,
adapter translations, factory labels/parameters, signature defaults, fallback
errors and metadata-budget exhaustion, old-provider refusal and config loaders.
The source capability remains unpublished. This proposal closes on completed
provider-source implementation and its guards; public-package release and
consumer receiving qualification remain separate claims.

The guard asserts both zero conversions and absent payloads, while preserving
native exception identity/cause/traceback and validation execution. It explicitly
skips capability-dependent cases on older providers; such a run qualifies only
compatibility, not restricted capture. Local qualification uses the pinned
SMonitor source above. Separate subprocess smoke checks against SMonitor tag
sources 0.16.0 and 0.18.0 verified detailed pipeline execution and explicit
restrictive refusal; those are source checks, not installed-package receiving
qualification.

The complete compatibility suite against tag source 0.16.0 passes 344 tests with
37 expected capability skips. That synthetic source substitution disables the
development environment's current `smonitor` pytest plugin (`-p no:smonitor`):
the plugin is newer than 0.16.0 and imports event-observer helpers absent from
that tag. The normal gate uses the installed provider's plugin and retains all
capture cases. This is not a clean published-artifact qualification.

Final local validation on Python 3.14 with the pinned provider source: 382 tests
passed without skips, including 42 capture cases and the explicit-selection
guards. Ruff lint/format, report-index and whitespace checks passed. Sphinx built
successfully with three existing heading warnings in `docs/index.md`.

## Resolution — 2026-10-06

Implemented in `4d708f92d9ee40870e40b251c60032d6c2ac76ca`, together with the
independent selector from `uibcdf/argdigest#30`. The capture guard protects the
original failure mechanism before formatting and verifies the preserved native
outcome. The existing SMonitor floor is unchanged; a restrictive request fails
closed when the installed provider lacks the scoped API. Closing this source
proposal does not assert that SMonitor or ArgDigest packages containing the new
capability have been published, or that Recorda has adopted them. Provider
publication remains owner-specific future release work; consumer applicability
and installed qualification remain with `uibcdf/recorda#2` and coordinated
member receiving work in `uibcdf/molsyssuite#106`.
