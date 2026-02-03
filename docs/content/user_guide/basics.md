# Basics

ArgDigest wraps functions with a `@arg_digest` decorator that can:

1) Digest individual arguments using **argument-centric digesters**.
2) Apply reusable **pipelines** by `kind` and `rules`.

## Argument-centric digestion

```python
from argdigest import arg_digest, argument_digest

@argument_digest("selection")
def digest_selection(selection, caller=None, syntax=None):
    if selection is None:
        return "all"
    return selection

@arg_digest(digestion_style="decorator", strictness="warn")
def get(molecular_system, selection=None, skip_digestion=False):
    return molecular_system, selection
```

## Pipeline-based validation

```python
from argdigest import arg_digest, register_pipeline

@register_pipeline(kind="feature", name="feature.base")
def feature_base(obj, ctx):
    if not hasattr(obj, "feature_id"):
        raise ValueError("Missing feature_id")
    return obj

@arg_digest(map={"feature": {"kind": "feature", "rules": ["feature.base"]}})
def register_feature(feature):
    return feature
```

## Explicit mapping with `arg_digest.map`

For explicit validation mapping (using pipelines), the alias `arg_digest.map` offers a cleaner syntax:

```python
from argdigest import arg_digest

arg_digest.map(
    feature={"kind": "feature", "rules": ["feature.base"]},
    # Pydantic models can be used directly as rules!
    user={"kind": "data", "rules": [User]} 
)
def register_feature(feature, user):
    return feature
```

## Standard Pipelines (Batteries Included)

ArgDigest comes with a set of built-in pipelines under the `std` kind. These are automatically
registered and ready to use.

```python
arg_digest.map(
    flag={"kind": "std", "rules": ["to_bool"]},
    indices={"kind": "std", "rules": ["to_list"]},
    path={"kind": "std", "rules": ["strip", "is_file"]}
)
def load_data(flag, indices, path):
    ...
```

Available standard rules include:
- **Coercers**: `to_bool`, `to_list`, `to_tuple`, `strip`, `lower`, `upper`.
- **Validators**: `is_positive`, `is_non_negative`, `is_file`, `is_dir`, `is_int`, `is_str`.

## Native Integrations

ArgDigest integrates seamlessly with the ecosystem if optional dependencies are installed.

### Pydantic Models as Rules
You can pass a Pydantic `BaseModel` class directly in the `rules` list. ArgDigest will automatically
validate and coerce the argument into that model.

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

arg_digest.map(user={"kind": "data", "rules": [User]})
def process_user(user):
    # 'user' is now an instance of User
    return user.name
```

### Beartype Type Checking
Use the `type_check=True` parameter to enforce type hints *after* digestion has occurred.

```python
@arg_digest(type_check=True) # Automatically applies @beartype
def calculate(a: int):
    return a

# calculate("10") works if digestion converts it to int.
# calculate("hello") fails with a Beartype error.
```

### PyUnitWizard (Science-Aware)
ArgDigest provides first-class support for physical quantities via `PyUnitWizard`.

#### 1. Quantity Pipelines
You can use factory functions from `argdigest.contrib.pyunitwizard_support` to create rules:

```python
from argdigest.contrib import pyunitwizard_support as puw_support

arg_digest.map(
    cutoff={
        "kind": "quantity", 
        "rules": [
            puw_support.is_quantity(),
            puw_support.check(dimensionality={'[L]': 1}),
            puw_support.standardize()
        ]
    }
)
def compute(cutoff):
    # cutoff is now a standardized Quantity object
    ...
```

#### 2. Automatic Context Management
You can set a temporary PyUnitWizard context (standard units, default form) for the duration
of a function call using the `puw_context` parameter:

```python
@arg_digest(puw_context={"standard_units": ["nm", "ps"], "form": "pint"})
def simulation(time):
    # Within this function, puw.standardize() uses nm/ps and pint
    ...
```

## Dual mode (argument digestion + pipelines)

If both are configured, argument digestion runs **first**, then pipelines are applied to the
updated values.

## Library-level defaults

To avoid repeating `digestion_source` and `digestion_style` in every decorator, a library can
define defaults globally.

### Option A: Configuration Module (File-based)

Define a module (e.g., `mylib/_argdigest.py`) and reference it:

```python
# mylib/_argdigest.py
DIGESTION_SOURCE = "mylib._private.digestion.argument"
DIGESTION_STYLE = "package"
STANDARDIZER = "mylib._private.digestion.argument_names_standardization:argument_names_standardization"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

```python
from argdigest import arg_digest

@arg_digest(config="mylib._argdigest")
def myfunc(...): ...
```

### Option B: Programmatic Configuration

You can set defaults programmatically, typically in your library's `__init__.py`:

```python
import argdigest.config

argdigest.config.set_defaults(
    digestion_source="mylib.digestion",
    digestion_style="package",
    strictness="error"
)

# Now @arg_digest() uses these defaults automatically
@arg_digest()
def myfunc(...): ...
```

If `@arg_digest()` is used without explicit configuration, ArgDigest will try to auto-discover
`<root_package>._argdigest` based on the decorated function's module. If not found, the
global defaults (set via `argdigest.config.set_defaults`) are used.
