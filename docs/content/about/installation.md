## Installation

ArgDigest can be installed via pip or conda (future).

### Basic Installation

```bash
pip install argdigest
```

### With Optional Dependencies

To enable seamless integration with **Pydantic**, **Beartype**, **Numpy**, and **Pandas**, install with extras:

```bash
# Install everything (recommended for most users)
pip install argdigest[all]

# Or pick specific integrations
pip install argdigest[pydantic]
pip install argdigest[beartype]
pip install argdigest[pyunitwizard]
```

These extras enable features like passing Pydantic models as rules, using `type_check=True`, or using specialized Data Science pipelines.

Install from source:

```bash
git clone https://github.com/uibcdf/argdigest
cd argdigest
pip install -e .
```
