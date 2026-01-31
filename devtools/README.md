# Devtools

This folder provides conda environment definitions and a conda-build recipe.

## Create conda environments

Development:

```bash
conda env create -f devtools/conda-envs/development_env.yaml -n argdigest-dev
```

Documentation:

```bash
conda env create -f devtools/conda-envs/docs_env.yaml -n argdigest-docs
```

Build tools:

```bash
conda env create -f devtools/conda-envs/build_env.yaml -n argdigest-build
```

## Build the conda package locally

```bash
conda activate argdigest-build
conda build devtools/conda-build
```

The `meta.yaml` uses `GIT_DESCRIBE_TAG` for the version. Ensure your git tags are set or
export the variable before building.
