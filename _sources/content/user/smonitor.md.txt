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
