---
summary: Select argument digestion independently of configuration and pipelines.
issue: uibcdf/argdigest#30
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: measured
area: [api, configuration]
guard: tests/test_argument_digestion_selection.py
normative:
blocked_by: []
supersedes: []
---

# Explicit argument digestion

## What

Supplying configuration participates in current automatic mode inference and
can activate missing-digester checks before an otherwise valid pipeline. This
is an API clarity proposal, not a claimed breach of prior compatibility.

## How

Add argument_digestion=None/True/False. None retains historical inference;
True enables argument-centric digestion and its strictness policy; False skips
only argument digester discovery/execution. Binding, normalization, function
contracts, pipelines and type checks remain active. The selector is available
inline, through the map alias, DigestConfig, modules and files; the plan exposes
both selection and effective enable_argument_digestion.

## Why

Discovery style and execution selection answer different questions. A boolean
selector with None for compatibility avoids another discovery style or policy
engine, and allows diagnostic/profiling configuration without accidental mode
changes when a consumer selects pipeline-only processing explicitly.

## Acceptance criteria

- Equal explicit selection yields equal inline/configured behavior.
- True retains strict missing-digester refusal; None retains published defaults.
- False retains signature/contract/normalization/pipeline/type invariants.
- False does not import unselected argument sources.
- Classmethods, positional-only and var-positional signatures keep call shape.
- Config/file/agent introspection describes requested and effective selection.

## Local implementation

The selector is implemented in the owning configuration/decorator modules and
exposed by both decorator forms. Plans and CLI audit distinguish requested and
effective selection; generated contributor guidance includes the default.

The guard reproduces the original configuration-dependent behavior under None,
compares both explicit modes across inline/config/map transports, and verifies
that False retains contract/alias/standardizer/type-check and signature behavior.
An unavailable digestion source is not imported in that mode. File and module
loaders, explicit override precedence, invalid selectors and digester-before-
pipeline ordering are covered. Publication and receiving work are separate
from the completed source proposal.

Final local validation: all 24 selection cases passed within the complete
382-test suite, including combined restrictive capture plus pipeline-only
configuration. Lint/format, generated guidance, offline report indexes and
documentation build were checked alongside the capture proposal.

## Resolution — 2026-10-06

Implemented in `4d708f92d9ee40870e40b251c60032d6c2ac76ca`. The guard protects
configuration-independent explicit selection and preserves the original
inference under None, strict missing-digester refusal under True, and mandatory
contract/pipeline behavior under False. Both source APIs and maintained guidance
are complete. Package publication is future owner-specific release work;
consumer applicability and installed qualification remain with
`uibcdf/recorda#2` and `uibcdf/molsyssuite#106`.
