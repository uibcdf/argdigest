# Devtools

This folder provides conda environment definitions and a conda-build recipe.

## Explicit SMonitor nested-signal receiving

ArgDigest #49 owns reception of SMonitor #59/#61. After selecting an exact
provider source or published file and verifying its installed import origin, run:

```bash
python -m pytest --receptor=llm devtools/tests/receive_smonitor_nested_signals.py
```

The 28 controls assert actual handler/history outcomes, native and catalog
exception preservation, nested ERROR deduplication, application policy and
restrictive capture. Pipeline and call-shape failures exercise validation before
the function body. The module has no skip or provider-version detection.

Its `receive_` filename makes this a separately selected receiving gate: ordinary
tests and the historical installed-core/full profiles retain their existing
provider contracts. Adding this gate to a public profile needs a published
corrected provider and the normal profile review. Source/private-wheel success
does not establish public availability or a new runtime minimum.

For installed receiving, copy the module outside the checkout and run the
selected environment's Python there with `-P -m pytest --import-mode=importlib
-c /dev/null --receptor=llm -o 'receptor_rerun_command=python -m pytest'` and the
copied module path. Preserve source identities, artifact hashes, import origins,
command exits and outcomes in the owning report. Repeat against the actual
published file before making a public adoption claim.

## Create conda environments

Development:

```bash
CONDA_CHANNEL_PRIORITY=strict conda env create -f devtools/conda-envs/development_env.yaml -n argdigest-dev
```

Documentation:

```bash
CONDA_CHANNEL_PRIORITY=strict conda env create -f devtools/conda-envs/docs_env.yaml -n argdigest-docs
```

Build tools:

```bash
conda env create -f devtools/conda-envs/build_env.yaml -n argdigest-build
```

## Review dependency routes before tests and candidate builds

`dependency_routes.toml` classifies the maintained recipe, environments and
workflows. Requirements remain in `pyproject.toml`. Use a clean MolSysSuite
clone at the inventory's full `shared_tool.commit`:

```bash
python -B /path/to/pinned/molsyssuite/devtools/scripts/dependency_routes.py \
  --root /path/to/argdigest --inventory devtools/dependency_routes.toml
```

The normal CI runs this shared command before the test job. The publication
decision runs it against the exact candidate before permitting the existing
shared build workflow. New routes or changed workflow bytes require a reviewed
inventory update; do not refresh hashes automatically. Unsupported layouts need
an owned profile. This is an offline input check, not a solver or scientific
qualification. The build-only environment remains outside runtime comparison.

## Candidate publication

Use `.github/workflows/build_and_upload_conda_packages.yaml` with the reviewed
full candidate SHA and matching committed plan version. The plan selects
staging or the authorized direct route; source gates, occupied-coordinate
checks, exact archive/resource inspection and installed qualification remain
mandatory. Promotion uses the original tested file and digest.

The recipe gets `MOLSYSSUITE_CONDA_VERSION` and
`MOLSYSSUITE_CONDA_BUILD_NUMBER` from the shared publisher. It freezes the
version only in its ephemeral build clone. A bare local `conda build` does not
provide that reviewed route or authorize publication. The complete review and
original public 0.14.0 evidence are tracked in `uibcdf/argdigest#28` and
`uibcdf/argdigest#24` respectively.
