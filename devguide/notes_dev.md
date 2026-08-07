# Development Notes

## Current state snapshot

- Current stabilization tag: `0.9.2` (final pre-1.0 checkpoint).
- Core decorator: `arg_digest` supports argument-centric, pipeline-centric, and mixed modes.
- Config model: explicit args, config module (`_argdigest.py`), env override (`ARGDIGEST_CONFIG`), and auto-discovery.
- Diagnostics: catalog-backed errors/warnings integrated with smonitor.
- Optional integrations: beartype, pydantic, pyunitwizard.
- Examples: `examples/packlib` and `examples/reglib` used for smoke tests and docs.
- Packaging uses setuptools package discovery (`include = ["argdigest*"]`) to keep
  subpackages in release wheels.
- CI/docs workflows include strict import smoke checks that fail hard on import errors.
- CLI includes `argdigest health-check` for ecosystem diagnostics.
- Current local test status baseline: full suite green.

## Test status

- Full suite currently passes.
- Known warning pattern: tests using pipelines without digesters may emit
  `DigestNotDigestedWarning` when strictness is `warn`.

## Recent implementation note

- Added `argdigest.core.caller.normalize_caller`, `argdigest.core.caller.caller_matches`, `argdigest.core.caller.caller_is_one_of`, and `argdigest.core.caller.caller_startswith` as lightweight helper APIs for downstream digester authors.
- What changed in practice: downstream digesters can now express callable-specific optional semantics without open-coding fragile string logic such as repeated `caller.endswith(...)` or ad-hoc `caller.startswith(...)` branches.
- Why this was necessary: MolSysMT now exposes `MolSysBuilder` and `build.editable(...)` as normal public APIs. Those APIs legitimately accept values such as `molecular_system=None`, `atom_type=None`, `group_type=None`, or `entity_name=None` depending on the callable. Treating these as exceptional cases outside digestion would have weakened both ArgDigest and the downstream API contract.
- Design decision: the correct place to solve this is the digestion layer, not the downstream API. ArgDigest therefore grows a slightly richer caller helper surface while keeping the public top-level API stable.
- These helpers remain outside the top-level public surface so the stable `argdigest.__all__` contract does not change during the pre-1.0 hardening window.

## Recent implementation note — axis 1, the function argument contract

- Added `argdigest.core.function_contract` (`Domain`, `FunctionContract`, resolution and
  checking) and `argdigest.core.function_loader` (discovery), plus the
  `unknown_argument` policy, the `FUNCTION_SOURCE` / `DOMAIN_SOURCE` configuration, and
  the `UnknownArgumentError` / `MissingArgumentError` / `ArgumentConsistencyError` /
  `FunctionContractWarning` catalogued diagnostics.
- What changed in practice: ArgDigest covered one axis only — *given an argument name, is
  its value valid?* It had no way to ask *may this function receive this argument at
  all?*, and `bind_arguments` silently discarded any keyword a closed signature did not
  declare. A mistyped argument therefore ran with the default and returned a plausible
  wrong answer. Measured in MolSysMT: a one-letter slip in `structure_indices` returned
  all 5000 structures of a trajectory instead of the three requested, with no
  diagnostic. 22 of its 26 public callables behaved that way, and the other four failed
  with a raw `KeyError` or a `TypeError` naming a private converter.
- Why this was necessary now: **ArgDigest was more permissive than the language it
  wraps.** Plain Python raises `TypeError` for an unexpected keyword; a decorated
  function accepted it. Stabilizing `1.0.0` on top of that would have frozen the
  anomaly into the contract every downstream library depends on.
- Design decision: the consumer declares only data — a `Domain` pointing at its own
  source of truth and a `FunctionContract` per function or family. Discovery, the
  resolution order (exact caller, then longest matching pattern, then default),
  enforcement, diagnostics and introspection stay in ArgDigest. A closed signature is
  held to its own parameters with no declaration at all, which is why MolSysMT gained
  protection on 19 functions without writing a rule for any of them.
- Continuity with the previous note: `caller.endswith(...)` in downstream digesters,
  which the `argdigest.core.caller` helpers made safer to write, was the symptom of this
  missing axis. Function-dependent rules had nowhere to live and lodged inside
  per-argument digesters — 102 of MolSysMT's 392 branch on `caller`. Axis 1 gives those
  rules a home; the helpers remain the right tool for the value-digestion cases that
  legitimately depend on the caller.
- Known gap: a *delegating* domain, whose admissible keywords depend on values resolved
  at call time (a converter chosen by `to_form`, for instance), is not expressible,
  because a `Domain` decides membership from the keyword alone. Such functions keep the
  permissive default. `molsysmt.basic.convert` is the live example.
- Evidence: 148 ArgDigest tests, ~8300 MolSysMT tests with the policy set to `error`
  plus its fast release gate at 12/12, and 1296 MolSysViewer tests with nothing declared
  on its side. No downstream call in either consumer had to change, which is what a
  defect that only reaches users looks like.

## Open technical items

- Keep collective status aligned with sibling repos and `../molsyssuite/devguide/collective_v1_checklist.md`.
- Hold `1.0.0` tag until explicit release-owner confirmation.

## 1.0.0 path alignment

- `0.6.x`: integration hardening (closed).
- `0.7.x`: API freeze (closed).
- `0.8.x`: release candidate stabilization (closed).
- `0.9.x`: RC consolidation (active).
- `1.0.0`: stable release.

See `devguide/ROADMAP.md` for full milestones and exit criteria.
