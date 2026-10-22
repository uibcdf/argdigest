---
summary: Allow an explicit contract lookup owner independently of runtime method display.
issue: uibcdf/argdigest#37
status: open
opened: 2026-10-22
closed:
verification: reproduced
area: [contracts, inheritance, integration]
guard:
normative:
blocked_by: []
supersedes: []
---

# Declared contract owner

## What

Consider an opt-in declaration of the contract lookup key for inherited methods,
while retaining the runtime class in diagnostic `qualname`. Preserve the default
runtime-owner rule used by mixin consumers. This is an additive API proposal;
it does not establish that the current documented behavior is a regression.

The motivating consumer defect, `uibcdf/molsysmt#404`, is closed. MolSysMT now
passes `native_constructor` through the existing decorator-context mechanism to
seven native count digesters. This preserves their validation and closed
constructor signatures. It does not select ArgDigest's normalization tables,
standardizer or function/domain contracts under a declared base key.

## How

Triage used source `c5a85ade29c409177d33f7529885bd71bf2736ee` imported from
the primary checkout on Python 3.14.7. A separate-process probe defined a
module-level `owner37.base.Base.accept` and an inherited class with
`__module__="owner37.child"`, registered identity digesters, and declared:

- `FunctionContract(caller="owner37.base.accept", mutually_exclusive=[("x", "y")])`;
- `AliasTable({"short": "value"}, applies_to="owner37.base.accept")`;
- decorator context `native_constructor="owner37.base.accept"`.

The base digester received `caller="owner37.base.accept"`; the inherited call
received `caller="owner37.child.accept"` and
`qualname="owner37.child.Child.accept"`. Both received the same explicit
`native_constructor`. The base rejected simultaneous `x` and `y` and normalized
`short=7` to `value=7`. The inherited call used its runtime key: the base-specific
contract and alias did not match, and the existing default contract applied.
Thus custom digester context does not reselect the preceding contract stages.

Owning code is `argdigest/core/decorator.py`: `_resolve_owner_module`, the
wrapper's `caller` construction, normalization, standardizer dispatch,
`_enforce_function_contract` and digester argument injection. Extend these
existing consumers of one resolved key rather than adding a consumer-specific
constructor special case. `core/caller.py` currently supplies matching helpers,
not a declared-owner resolution policy.

The related selection passes 75 tests across `test_qualified_caller.py`,
`test_caller_helpers.py`, `test_function_contract.py` and
`test_normalization_rules.py`. Current qualified-caller fixtures define local
classes; new inheritance guards must also define methods at module scope so
they exercise the runtime-owner branch that excludes `<locals>`.

## Why

A single explicit contract identity could keep value digestion, normalization
and function admission coherent across inheritance without duplicating consumer
workarounds. Automatic changes to the default key could break existing mixins.
MolSysMT's bounded repair removes the immediate constructor blocker, so this
proposal does not require an emergency ArgDigest release or reopening #404.

## Acceptance criteria

- Decide the public declaration and exact-key semantics before implementing it;
  no proposed option name or value format is accepted by this triage.
- Preserve default caller resolution, mixin behavior and runtime `qualname`.
- Apply the explicit identity consistently to normalization, standardizers,
  function/domain contract selection and per-argument digester `caller`.
- Keep the declaration outside the wrapped function's caller-controlled inputs;
  retain signature binding, validation and unknown-argument refusal.
- Review compatibility with existing arbitrary decorator context names before
  reserving any new keyword. Cover invalid declarations and introspection.
- Test module-level inheritance, multiple inheritance/mixins, overrides,
  classmethods and staticmethods, including unchanged behavior without opt-in.
- Qualify consumer receiving separately; source support alone does not establish
  adoption by MolSysMT or justify removing its existing workaround.
