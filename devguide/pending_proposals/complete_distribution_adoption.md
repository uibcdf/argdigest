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
