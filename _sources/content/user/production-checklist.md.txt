# Production Checklist

Use this checklist before releasing a library that integrates ArgDigest.

## Integration contract

Before release, ensure the integration contract is explicit. `_argdigest.py`
should exist, be documented for contributors, and reflect a stable digestion
style choice. `strictness` should also be intentional: mature code paths are
usually expected to run with `error`.

**Both axes must be declared.** An integration that covers only argument digesters
leaves half its surface unguarded:

- [ ] every public callable is decorated — an undecorated entry point is a second door
      into the library that skips digestion entirely;
- [ ] every function taking `**kwargs` declares the domain of those keywords; until it
      does, it admits anything, and a mistyped keyword is silently discarded while the
      call runs with the default;
- [ ] `UNKNOWN_ARGUMENT` is intentional, and `error` before release;
- [ ] inter-argument rules live in contracts rather than as `raise ValueError` inside
      function bodies, so they reach the diagnostics catalogue.

Closed signatures need no declaration: they are held to their own parameters
automatically. The checklist item above is only about the functions that opened their
door on purpose.

## Runtime behavior

Every public API entry point should be decorated — not only the ones that seemed to need
it, since an undecorated callable is a door into the library that skips both axes.
Aliases should be normalized consistently, and repeated validation semantics should be expressed
through reusable pipeline rules instead of scattered inline checks.

## Testing

Tests should cover both happy paths and invalid input behavior for migrated
functions. Missing-digester behavior must be explicitly tested, and at least one
smoke test should validate the full decorated call flow end to end.

Add one test that a mistyped keyword is refused. It is the cheapest guard against the
defect this whole mechanism exists to prevent, and it fails loudly if someone widens a
signature or drops a declaration.

## Diagnostics and docs

Error messages should include actionable context, and documentation/examples must
match current runtime behavior. Showcase pages are especially important because
integrators use them as copy/adaptation references.

## Release readiness

Release is ready when local tests pass, documentation builds cleanly, and
migration notes for downstream integrators are updated and coherent with the
current contract.
