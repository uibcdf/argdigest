# Devtools

This folder provides conda environment definitions and a conda-build recipe.

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
