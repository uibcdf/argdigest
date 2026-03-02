# Troubleshooting

Use this page for fast diagnosis of common integration failures.

## Decorator runs but digesters are never called

This usually means discovery is misconfigured. In most cases, either
`digestion_source` points to the wrong module/package, `digestion_style` does
not match the actual layout, or digester names do not follow the required
`digest_<argument>` pattern.

## Missing-digester warnings are noisy

Noisy warnings typically indicate migration is in progress without clear
prioritization. Confirm which arguments are intentionally raw, then cover
high-frequency arguments first. Keep `strictness="warn"` as a temporary
migration setting, not a permanent endpoint for mature modules.

## Standardizer is not applied

If standardization seems ignored, verify the standardizer is actually configured
in the decorator or `_argdigest.py`, confirm the callable signature is
`(caller, kwargs)`, and make sure it returns a dictionary instead of relying on
in-place side effects.

## Pipeline rule is registered but not found

When a pipeline rule cannot be found, the root cause is often one of three:
`kind`/`name` mismatch, registration code not executed before the decorated
function call, or circular imports that hide registration side effects.

## Circular digestion dependency error

A cycle means two or more digesters depend on each other in a closed loop.
Break the loop by making one argument independent, or move shared logic to a
pipeline step where ordering is explicit and easier to reason about.

## Practical debugging strategy

When in doubt, reduce scope first: test one decorated function with minimal
inputs, confirm discovery and standardization, then re-enable pipelines and
cross-argument dependencies. This stepwise approach isolates the failing layer
quickly.

## Next

Run the [Production Checklist](production-checklist.md) before release.
For user-facing message interpretation, see
[For End Users of Integrating Libraries](end-users.md).
