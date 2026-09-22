# Installation

ArgDigest is released on the `uibcdf` conda channel. There is no PyPI release yet, so
`pip install argdigest` does not work; from source it installs like any other package.

## Basic Installation

```bash
conda install -c uibcdf -c conda-forge argdigest
```

Both channels are needed: `depdigest` and `smonitor` come from `uibcdf`, the rest from
`conda-forge`.

## With Optional Dependencies

The conda package carries the runtime dependencies only, so the integrations with
**PyUnitWizard**, **Pydantic**, **Beartype** and **Pandas** are installed alongside it:

```bash
conda install -c uibcdf pyunitwizard
conda install -c conda-forge beartype pydantic pandas
```

These enable features like passing Pydantic models as rules, using `type_check=True`, or
using the specialized data-science pipelines.

## Install from source

```bash
git clone https://github.com/uibcdf/argdigest
cd argdigest
pip install -e .
```

From a source checkout the same integrations are declared as extras:

```bash
# Everything at once
pip install -e ".[all]"

# Or pick specific integrations
pip install -e ".[pydantic]"
pip install -e ".[beartype]"
pip install -e ".[pyunitwizard]"
```
