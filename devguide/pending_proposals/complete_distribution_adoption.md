---
summary: Complete the distribution contract review and preserve required provider floors in runtime environments.
issue: uibcdf/argdigest#28
status: partial
opened: 2026-10-06
closed:
verification: reproduced
area: [distribution, governance]
guard: tests/test_compatibility_matrix.py::test_runtime_environments_preserve_required_provider_floors
normative: MOLSYSSUITE_GUIDE.md
blocked_by: []
supersedes: []
---

# Complete distribution adoption

## What

The review in uibcdf/molsyssuite#45 found that development, documentation and
routine-test Conda environments omitted the already declared runtime minima:
`depdigest>=0.11.0` and `smonitor>=0.16.0`. Metadata, the Conda recipe and the
core-test environment already preserved these bounds. Installing the wheel
with `--no-deps` makes the routine-test environment responsible for supplying
compatible providers itself.

This correction adds the existing bounds to those six environment entries.
It leaves Python selections, channels, optional dependencies, runtime code,
metadata and public release 0.14.0 unchanged.

## How

The reviewed baseline is `42b2f93346fdcd1573ade66a3f82a1717a496184`.
The compatibility guard reads required provider floors from `pyproject.toml`
and checks four runtime-bearing environments: development, docs, routine
tests and core tests. `build_env.yaml` is classified separately as build
tooling. A new environment must receive an explicit local role before this
guard claims its contract.

The comparison accepts an equal or stricter explicit `>=` bound. Six
negative cases cover each provider being absent, unbounded or below its
metadata minimum. A separate positive case accepts stronger bounds; that
case verifies comparison semantics and does not claim solver availability.
This bounded parser covers the currently reviewed explicit `>=` constraints;
other constraint forms and complete route resolution need their own review.

Before the YAML correction, the affected administrative module returned
**three failed and nineteen passed**: precisely the development/docs/test
environment assertions failed. After correcting the six entries, it returned
**twenty-two passed** with native exit zero.

Local reproduction used Python 3.14.7 in `molsyssuite@uibcdf_3.14`:

```bash
python -m pytest --noconftest --receptor=llm tests/test_compatibility_matrix.py
```

`--noconftest` scopes this local run to static contracts, excluding the runtime
registry fixture. The normal hosted CI retains its existing fixtures and
selection. PyYAML is already declared in the test environment; `packaging`
comes from pytest's tool dependency closure. No runtime dependency was added.
The development workspace's previously recorded eight unrelated dependency
conflicts remain; this result is not scientific or workspace qualification.

The existing public artifact retains its original identity:
source `0fa776af2d271065c60727c28480b20c3ce09aee`, producer
[37210475369](https://github.com/uibcdf/argdigest/actions/runs/37210475369),
file `noarch/argdigest-0.14.0-py_0.tar.bz2`, SHA-256
`983dca0f6bd0944d81fb1efc01e1dfa5c951e95abac6e7a0a08a13b7370d3b9e`.
This administrative source correction neither rebuilds those bytes nor
inherits their executed qualification for a new candidate.

## Why

These are ArgDigest-owned input and regression corrections under the existing
shared distribution policy, rather than new shared requirements. Explicit
floors prevent the declared environments from silently permitting older
providers than the installed package supports.

## Acceptance criteria

- Correct and guard the six omitted provider minima (implemented locally).
- Inspect the applicable hosted gates on the published correction commit.
- Complete the remaining local whole-policy review: classify applicable
  public/source/development/optional routes, confirm their Python and provider
  contracts, and maintain runnable preflight and relevant negative cases.
- Keep publication access, adoption and exact-artifact qualification separate.
  The existing verified Conda delivery is evidence for that observed route,
  not future credentials or an additional public route.

The minimum-floor correction is a completed subset; the owning issue remains
open with overall distribution adoption **partial**.

## Complete route review — 2026-10-06

The accepted shared operation from uibcdf/molsyssuite#105 is reused at immutable
tool commit `43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc`; no local comparison
engine is added. `devtools/dependency_routes.toml` classifies all **17** routes:
one recipe, five environments and eleven workflows. It preserves metadata
authority and records complete workflow hashes to expose later route changes.

| Route | Reviewed contract |
| --- | --- |
| Public Conda recipe | One Python noarch file; required DepDigest/SMonitor and Python metadata agree; console entry point and six version/runtime resources use existing shared controls. |
| Development | Complete required runtime; reviewed Python 3.14 narrowing and strict channels. Removed one duplicate documentation tool declaration. |
| Documentation | Complete required runtime because Sphinx imports ArgDigest; supported Python 3.13 narrowing and strict channels remain. |
| Routine/core test tooling | Explicit Python `>=3.11,<3.15` bounds, required provider minima and workflow-selected supported cells. Exact `==` spelling retains the existing Pytest Receptor 1.1.0 and PyUnitWizard 0.27.0 tool versions. |
| Build bootstrap | Tools only; the recipe creates its own host environment. It does not install the ArgDigest runtime. |
| Required sibling source routes | Inapplicable: maintained member workflows acquire required SMonitor/DepDigest from public Conda. Editable ArgDigest is the subject package, not its own sibling dependency. Future source replacement requires a reviewed commit and installed provenance. |
| Optional scientific fixtures | PyUnitWizard/science/type-validation dependencies remain optional in metadata. Test fixtures and their existing release evidence do not become hard runtime dependencies. |
| Normal wheel/source CI | Explicit pinned offline preflight precedes the existing normal test job. Ordinary wheel/import/coverage and full-matrix selection are retained. Internal wheel testing is not a public PyPI route. |
| Candidate build wrapper | The same pinned preflight audits the exact checked-out candidate in the decision job, before the unchanged shared publisher can build. Existing source-gate/coordinate controls remain. |
| Installed full/core and promotion | Exact staged bytes, twelve full-installed cells, separate twelve-cell NumPy-free lower-bound core, and original producer/source/file verification retain ownership. The core artifact profile resolves exact staging/public coordinates with flexible priority and independent installed checks; it is distinct from ordinary strict tooling environments. |
| Documentation, policy and archival workflows | Actual install/admin/source-only routes have individual inventory reasons; no new package route is inferred. |

Runtime/environment bounds now pass the shared profile. Ruff retains its
existing 0.16.5 version with exact `==` spelling. No Python selection, supported
matrix cell, scientific test selection, runtime metadata or public artifact
changes. Normal CI and the candidate decision delegate directly to the shared
CLI; a local guard checks that both use the inventory's full provider commit
and that expensive jobs depend on these mandatory checks.

Local validation passes the 17 routes and 36 administrative compatibility,
publication and reporting tests. Provider-owned negative tests protect omitted
recipe requirements, stale floors/ceilings, unsupported Python, changed routes,
below-floor source versions, wrong installed provenance and archive resource/
embedded-version mismatches. The local guard is
`tests/test_noarch_conda_publication.py::test_dependency_preflight_precedes_tests_and_candidate_builds`.

The prior correction's ordinary CI `37441396269` passed 314 tests / one
unavailable sibling-integration skip. New input/caller changes still require
their own exact-head normal CI and policy checks. The current local workspace
check reports nine unrelated dependency findings (retained, not repaired here);
administrative validation does not establish joint dependency closure.

## Retained delivery and remaining acceptance

The claimed public route is `uibcdf` Conda, with optional science packages from
`conda-forge`; no public PyPI artifact or new delivery is claimed. The closed
uibcdf/argdigest#24 record retains the original twelve-cell source/installed/core
qualification, byte-preserving promotion and clean public Linux/Python 3.14
installation with matching archive resources, import origins, CLI and `pip check`.
That public-install result remains owner-measured evidence, separate from the
central independent original-file inspection and this current-source preflight.

Shared resource/archive and immutable-public-state negative guards are reused
rather than copied into ArgDigest. The generated version is frozen in the
ephemeral build; the core decorator, optional adapter, diagnostic catalog and
CLI are the other reviewed critical Python resources. No bundled native or
platform-generated payload requires another profile. Existing exact-file
installed and public poststate checks remain prerequisites of any new release.

The route review and invocation are implemented. Hosted exact-head caller
validation and final central adoption handoff remain; overall status stays
**partial** until that evidence is inspected. Provider acceptance alone does
not qualify these revised source inputs or transfer the old artifact's gates.
