# Development Notes

## Current state snapshot

- Latest tag: `0.11.0`. `main` carries seven commits beyond it, drafted in
  [`0.12.0_release_notes_draft.md`](0.12.0_release_notes_draft.md).
- Supported Python is `>=3.11,<3.14`, closed at both ends and held to the CI matrix by
  `tests/test_compatibility_matrix.py`.
- **There is one mechanism for not re-digesting a value: `skip_digestion`.** The
  `ValidatedPayload` passport is gone.
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

## Recent implementation note — call shape, and the passport removed (2026-08-12/13)

- **A decorated function is now called back the way it was declared.** `fn(**bound)` lost
  `*args` entirely and mishandled positional-only parameters; `core/utils.build_call`
  reconstructs the split, and `DigestionPlan.requires_call_shape` decides once at
  decoration time so signatures with neither feature pay nothing. Reported from
  MolSysViewer; the suspected positional-only failure was confirmed and fixed by the same
  change. The var-positional digestion semantics — one tuple, one digester, named for the
  parameter — are now written down rather than discoverable from a warning.
- **`ValidatedPayload` is removed, not replaced.** Two live defects, both consequences of
  its shape: declared twice so the decorator could never match a payload from the
  PyUnitWizard pipelines, and honoured by argument *name* with no record of which
  verification it represented, so one library's claim silenced another's digester.
- **A replacement was built, measured, and declined.** Value certification by identity,
  claim bound to the issuing digester, 3.5 µs to issue and 0.46 µs to consult, 27 tests
  green. Declined because it asked every digester author to learn `by`, `guard` and
  `source` for a problem no consumer had — the mechanism it replaced had zero users
  across MolSysMT, MolSysViewer and PyUnitWizard. Preserved with its code in
  `pending_proposals/value_certification/`.
- **The root cause was not ours.** A digester cannot cheaply short-circuit because
  `puw.get_unit` costs 363 µs where pint's own attribute answers in 0.88, and the cost is
  flat with array size. Filed as a proposal in PyUnitWizard. **The lesson worth keeping:
  we nearly added a caching layer to compensate for a missing predicate upstream.**
- **And the upstream fix landed the same day, which settles it.** PyUnitWizard
  implemented the predicate: `puw.check(q, unit='nm')` went from 887 µs to 10.26, and
  MolSysMT's `digest_coordinates` from 0.659 ms to 0.026 on already-canonical input — 25x
  on the exact case certification was designed for, with nothing new for a digester
  author to learn. Declining the mechanism was not a trade-off; the alternative was
  simply better.
- **Measurement discipline paid twice, and cost once.** The one performance defect
  actually found (`uibcdf/molsysmt#147`, a digester on an internal predicate called 434
  times per user action) came from refusing to accept a benchmark's own diagnosis. But
  two of my own counts were wrong the same way — enumerating `(module, name)` pairs
  instead of object identities inflated 13 319 decorated callables to 26 519. Count
  identities.

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
