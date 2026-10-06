# SMonitor Integration

ArgDigest uses SMonitor as its diagnostics backend.

For many users, this is transparent: you call a function in a host library and
receive structured, actionable validation output when an input is not accepted.

## What SMonitor provides in practice

- Consistent warning/error formatting across libraries.
- Structured metadata (codes, tags, context) when available.
- Better traceability when reporting issues to maintainers.

## Is SMonitor optional in ArgDigest?

In current ArgDigest releases, SMonitor is a runtime dependency.

This means diagnostics wiring is always active in normal use.

## What you may see in a message

Depending on how the host library configures output, messages can include:

- a diagnostic code,
- argument name and invalid value context,
- a short hint about how to fix input,
- links to docs or issue trackers.

These fields help maintainers reproduce and resolve problems faster.

## Do I need to configure SMonitor directly?

Usually no.

If you are integrating ArgDigest in your own library and need custom behavior,
configure SMonitor at the library level and keep catalog definitions in:

- `your_lib/_private/smonitor/catalog.py`
- `your_lib/_private/smonitor/meta.py`
- `your_lib/_smonitor.py`

For contributors working on ArgDigest itself, see the developer page:
[SMonitor integration](../developer/smonitor.md).

## Restrict collection before validation

Use `capture_policy="metadata_only"` when a boundary must not automatically
format argument values or native failures:

```python
from argdigest import arg_digest


@arg_digest.map(
    capture_policy="metadata_only",
    profile={"kind": "std", "rules": ["strip", "is_str"]},
)
def configure(profile):
    return profile
```

The option delegates to SMonitor's public `CapturePolicy` and `diagnostic_scope`.
`None` inherits the application's active scope and preserves detailed defaults
outside a scope. `"detailed"` requests detailed permissions but cannot relax a
stricter enclosing scope. A SMonitor `CapturePolicy` instance is also accepted.
Both decorator construction and the outermost digestion signal run under the
selected policy; registry calls and explicit failure events inherit it.

Restrictive capture prevents ArgDigest-owned diagnostic `repr`/`str` operations,
omits native error text and free-text details, and emits fixed catalog messages
with bounded public caller/argument identity when available. Values and `all_args`
remain available to validators through their normal `Context`; they are not
serialized into events. Contracts, aliases, digesters, pipelines and profiling
remain active. It is independent of `skip_digestion`.

Direct callable failures retain their original exception, cause and traceback.
Adapters retain their existing translated error types and original cause, using
fixed messages in restrictive mode. Diagnostic emission failures attempt a fixed
catalog fallback warning; a failed or promoted fallback cannot replace the
operation's outcome. Validation warnings promoted to errors still follow Python's
normal warning policy.

The policy spans the wrapped function's synchronous call. It does not govern
arbitrary formatting inside user validators or independently implemented
providers. ArgDigest does not await async bodies or drive generator iteration;
place an application scope around those executions. Async tasks inherit
SMonitor's context at creation. Thread-pool callers must propagate an ambient
scope explicitly with a fresh `copy_context().run` per submission; a per-decorator
policy applies when that decorator is invoked in any thread.

### Provider availability

The last verified public SMonitor release, 0.18.0, does **not** provide scoped
capture. The API is implemented at SMonitor commit
`6feac9728cc35d57cbc92f284d7040d7f04cb35b` under `uibcdf/smonitor#37`/#38.
Qualification against that source is not public-package compatibility.
Explicit restrictive selection raises `DigestError` with code
`ARG-ERR-CAPTURE-001` when the installed provider lacks the capability; ArgDigest
never silently substitutes detailed capture or changes global configuration.
Existing detailed use retains the declared SMonitor dependency floor.
Publication and receiving qualification remain tracked by
`uibcdf/argdigest#29` and `uibcdf/molsyssuite#106`.
