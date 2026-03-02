# Digestion Styles

ArgDigest supports multiple discovery styles so each library can keep its own
architecture.

## 1) Package style

Digesters are discovered from a package with one module per argument:

```text
mylib/_private/digestion/argument/
  selection.py      -> digest_selection(...)
  syntax.py         -> digest_syntax(...)
```

Use when:
- you want explicit, file-per-argument organization,
- many contributors will touch digestion logic.

This style is often the easiest to maintain over time in scientific libraries
because each argument has a clear home and ownership is naturally distributed.

## 2) Registry style

Digesters are collected in a dictionary mapping argument name to function:

```python
# mylib/_private/digestion/registry.py
ARGUMENT_DIGESTERS = {
    "selection": digest_selection,
    "syntax": digest_syntax,
}
```

Use when:
- you prefer a single explicit index of active digesters,
- your digestion surface is medium-size and centrally maintained.

Registry style is especially useful when teams want one place to audit coverage
quickly and keep strong control over what is active.

## 3) Decorator style

Digesters register themselves with `@argument_digest(...)`:

```python
from argdigest import argument_digest

@argument_digest("selection")
def digest_selection(selection, caller=None):
    ...
```

Use when:
- digesters live near feature code,
- plugin packages register digesters dynamically.

Decorator style can reduce wiring in modular systems, but it benefits from clear
import discipline so registrations are always loaded when expected.

## 4) Mixed style (`auto`)

ArgDigest can combine discovery sources when `digestion_style="auto"`.

Use when:
- you are migrating a legacy codebase incrementally,
- you need compatibility with more than one style during transition.

Mixed mode is best treated as a transition strategy rather than a permanent
architecture. It is powerful during migration, but should converge to a stable
long-term style when coverage is complete.

## Choosing a style

- Large scientific libraries: package or mixed.
- Compact libraries: registry.
- Plugin-heavy ecosystems: decorator or mixed.

## Next

Continue with [Auto Mode and Conflict Resolution](auto-and-conflicts.md).
