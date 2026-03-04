# Development Environment

Use the project conda environment for local development and tests.

## Environment bootstrap

Use the environment files under `devtools/conda-envs/`:
- `development_env.yaml` for daily development,
- `test_env.yaml` for test-focused execution,
- `docs_env.yaml` for documentation builds.

Typical bootstrap:

```bash
conda env create -f devtools/conda-envs/development_env.yaml
conda activate argdigest@uibcdf_3.12
```

If your local environment naming convention differs, keep the YAML files as
source of truth and map names locally.

Then install in editable mode:

```bash
python -m pip install --no-deps --editable .
```

## Daily commands

```bash
pytest
```

Build docs locally (from `docs/`) when editing documentation:

```bash
make html
```

Optional package sanity checks:

```bash
python -m pip check
python -c "import argdigest; print(argdigest.__version__)"
```

## Notes

- Keep Python version aligned with supported matrix.
- Prefer reproducible conda env files over ad-hoc local installs.
