---
summary: NumPy is loaded by consumers that never use scientific pipelines.
issue: uibcdf/argdigest#15
status: resolved
opened: 2026-09-22
closed: 2026-09-26
severity: medium
verification: reproduced
area: [dependencies, pipelines]
guard: tests/test_numpy_optional.py::test_core_import_and_standard_pipeline_do_not_load_numpy
normative: standards/ARGDIGEST_GUIDE.md
blocked_by: []
supersedes: []
---

# NumPy is loaded by non-scientific consumers

## What

ArgDigest declared NumPy as a required dependency and imported it while loading the
package's standard pipeline registry. A consumer using only strings and paths therefore
installed and loaded a compiled scientific library it did not use. This was reported from
`uibcdf/ackredit#62`.

## How

NumPy is now in the `science` extra instead of the core dependencies in both
`pyproject.toml` and the Conda recipe. The `data` and
`sci` modules register their pipelines without importing NumPy; NumPy loads only when
an array pipeline runs. The `pyunitwizard` extra retains NumPy because that integration
uses it. A missing NumPy error names `argdigest[science]`.

## Why

The default installation and import path should reflect the cost of the base argument
contract, while scientific consumers can opt into their required array support.

## Evidence

The guard runs a fresh Python interpreter with NumPy imports deliberately blocked. It
imports ArgDigest, exercises a standard boolean coercer, confirms NumPy stayed unloaded,
and checks that a scientific pipeline reports the missing extra. The package metadata
test asserts that the core dependency list excludes NumPy and the science extra includes
it. The Conda recipe compatibility test and focused pipeline tests passed on Python 3.13
on 2026-09-26.

## What was refuted

Moving only the import would leave every consumer installing NumPy. Moving only the
dependency would break package import because `science.py` used `np.float64` as a default.

## Scope and exclusions

This change does not alter array coercion or require scientific consumers to remove
NumPy. It changes the installation contract for the next release, not existing tags.

## Acceptance criteria

- Core installation metadata has no NumPy requirement.
- Core import and standard pipelines work without NumPy loaded or installed.
- Array pipelines still work when NumPy is installed and explain the science extra when
  it is absent.
- The canonical guide tells consumers when to install the extra.
