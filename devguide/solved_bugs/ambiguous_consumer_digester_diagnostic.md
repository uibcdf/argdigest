---
summary: Attribute ambiguous digester signatures to their consumer registration.
issue: uibcdf/argdigest#50
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: low
verification: reproduced
area: [diagnostics, digestion, integration]
guard: tests/test_consumer_digester_diagnostics.py
normative:
blocked_by: []
supersedes: []
---

# Ambiguous consumer digester diagnostic

## What

The supplied registry reproduction correctly refuses an ambiguous consumer
signature but uses ARG-ERR-MISS-001, loses the consumer/argument context and
asks for an upstream ArgDigest report. This is a registration error in the
consumer, not evidence of an internal library defect.

## How

Keep the exact DigestNotDigestedError family and refusal. Its ambiguous-signature
case now selects ARG-ERR-DIGESTER-001 with the actual consumer and argument,
digester identity and declared parameter names. The hint names the corrective
rule: explicitly name the value parameter after the registered argument when
additional dependency/context parameters exist. Valid single-candidate and
exact-name inference are unchanged; the corrected consumer executes normally.

The owning metadata helper accepts caller context without caching failures or
caller-specific errors. It never renders inspect.Signature, defaults, annotations
or values. Restrictive capture uses fixed catalog wording. The normal wrapper
passes its runtime display identity; no consumer-side workaround is added.

Against exact old ArgDigest 5b61925, seven of eight new controls fail on the
wrong code or absent context. All eight pass after correction, as do 58 focused
diagnostic/decorator/capture controls and the complete 528-test local source
selection including collective E2E and nested-signal receiving. Three known
missing-digester warnings remain. The local source environment inherits editable
siblings; this is not the subsequent public release's clean installed proof.
Release ownership is uibcdf/argdigest#51, with independent exact-candidate/file
gates and publication evidence required there.

## Why

The guard asserts attribution and correction in user/dev/qa profiles, detailed
and restrictive capture, zero default conversion, per-consumer failure context,
unchanged error family and successful corrected registration. It protects the
reported mechanism rather than merely checking rendered words. Delivery of
0.17.1 remains separately qualified; the #9 typing proposal remains deferred.
