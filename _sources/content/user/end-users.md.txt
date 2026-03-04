# For End Users of Integrating Libraries

Most people who benefit from ArgDigest do not use it directly. They use a host
library that integrates ArgDigest and encounter its validation messages during
normal workflows.

This page explains how to interpret those messages and what to do next.

## What these messages usually mean

When an input is invalid or ambiguous, ArgDigest-based validation often reports:
- the argument name,
- the received value,
- the function or call context,
- a hint about valid input shape.

The goal is to make failures understandable and actionable, not to expose
internal implementation details.

## How to react to a validation message

First, read the argument and hint carefully and adjust your input according to
the documented API of the host library. In many cases, the issue is a type
mismatch, unsupported value, or ambiguous selector.

If the same input worked in a previous release, check release notes and
migration guides from the host library before reporting an issue.

## When to contact maintainers

Report to maintainers when:
- the message is unclear or inconsistent with the public API,
- the hint suggests a valid format that still fails,
- behavior differs between similar entry points unexpectedly.

Useful report payload:
- library version,
- minimal reproducible call,
- full message text,
- expected behavior.

## Two practical examples

### Example 1: wrong type

You call a function with `selection=10`, but the host library expects a string
selector in that context. A typical message will identify `selection`, show the
received value, and provide a hint about the accepted form. The practical fix is
to pass the selector in the expected format (for example, a supported string
expression) according to the host-library API docs.

### Example 2: ambiguous alias

You pass `name="CA"` in a call path where the library expects a more specific
argument such as `atom_name`. A normalization or digestion message may indicate
that the provided alias is ambiguous or unsupported in that context. The fix is
to use the explicit argument name documented for that function.

## Version changes and stricter validation

As host libraries mature their ArgDigest integration, validation may become
stricter across releases. Inputs that previously passed with warnings can become
hard errors when contracts are enforced more strictly. This is expected in many
migration paths.

When this happens:
- check host-library release notes and migration notes,
- update your input format to match the new documented contract,
- report only if behavior contradicts the published API.

## About SMonitor-formatted output

Some libraries emit ArgDigest-related diagnostics through SMonitor. In that
case, messages may include codes, tags, or structured metadata. These fields are
intended to improve support and triage, but the core action remains the same:
fix input according to the API contract, or report a reproducible mismatch.

For a focused overview of diagnostics behavior, see
[SMonitor Integration](smonitor.md).
