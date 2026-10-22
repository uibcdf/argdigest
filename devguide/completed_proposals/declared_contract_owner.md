---
summary: Allow an explicit contract lookup owner independently of runtime method display.
issue: uibcdf/argdigest#37
status: resolved
opened: 2026-10-22
closed: 2026-10-22
verification: reproduced
area: [contracts, inheritance, integration]
guard: tests/test_contract_owner.py
normative:
blocked_by: []
supersedes: []
---

# Declared contract owner

## Implementation — 2026-10-22

The maintainer authorized implementation, then requested a comparison of design
tradeoffs. The accepted implementation uses `DigestConfig.contract_owner`:
`None` retains runtime resolution, `"definition"` resolves each decorated
function's defining `module.name`, and an exact dotted key selects a logical
owner. Definition mode avoids repeating names and permits one configuration
to serve multiple methods and independently decorated overrides. Exact keys
remain useful for mixins whose logical owner differs from their source module;
their spelling must be maintained explicitly. Valid keys are not imported or
required to name an existing declaration; ordinary matching/fallback remains.

The field lives in configuration rather than reserving an existing arbitrary
decorator-context keyword. Existing `arg_digest(contract_owner=...)` context
continues to reach digesters. All configuration loaders and both decorator
forms support the policy. Module/file keys are `CONTRACT_OWNER` (Python) or
`contract_owner` (JSON/YAML). Invalid selections fail at configuration time.

`core/caller.py` owns independently tested validation and declaration-time
resolution. The wrapper consumes the one resolved key for alias tables,
standardizers, function/domain selection and digester `caller`. Runtime
`qualname` and explicit-policy contract-refusal display remain separate.
`digestion_plan.contract_owner` records the requested selection;
`digestion_plan.contract_caller` records its fixed resolution or None for
runtime dispatch. CLI audit and generated agent guidance expose the selection.

The guard contains 37 cases covering module-level external inheritance, deep
and multiple inheritance, overrides, both classmethod decorator orders,
staticmethods, shared aliases/standardizers/contracts/domain selection,
closed signatures, native value refusals, retained arbitrary context,
pipeline-only execution, all configuration transports and malformed keys.
It protects the mechanism reproduced in triage: a method can retain its base
contract key while diagnostic identity continues to name the runtime child.
The complete Python 3.14.7 source suite passes 431 tests without omissions.

This resolves provider source implementation. The code is development after
0.16.0; this work creates no new release/tag and does not adopt the option in
MolSysMT. Its existing `native_constructor` workaround remains consumer-owned
until a separately qualified receiving decision.
Shared impact and consumer receiving are tracked in `uibcdf/molsyssuite#123`.

## Initial triage — 2026-10-22

The following analysis and acceptance criteria record the pre-implementation
proposal; the implementation decision above supplies the selected public API.

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
