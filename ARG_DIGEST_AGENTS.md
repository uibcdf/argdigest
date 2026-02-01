# ArgDigest Agent Instructions for argdigest

This document provides context and instructions for AI Agents (like yourself) to maintain and use **ArgDigest** within this project.

## 1. Project Context
- **Library Module**: `argdigest`
- **Digestion Style**: `auto`
- **Digestion Source**: `None`
- **Standardizer**: `None`
- **Strictness Level**: `warn`
- **Bypass Parameter**: `skip_digestion`
- **PUW Context**: `None`

## 2. Your Mission as an Agent
Whenever you modify or add a function in this library:
1. **Apply Digestion**: Ensure the function is decorated with `@argdigest.digest()`.
2. **Check Arguments**: If you add new arguments, check if they need a specific digester in the `digestion_source` directory.
3. **Use Pipelines**: For specific validation (e.g. ranges, types), use `@digest.map` with appropriate rules.
4. **Maintenance**: If you change the ArgDigest configuration (e.g. adding a standardizer), you **MUST** run `argdigest agent update --module argdigest` to keep this file in sync.

## 3. Available Resource Library (Don't Re-invent)

### Standard Pipelines (`std` kind)
- **Coercers**: `to_bool`, `to_list`, `to_tuple`, `strip`, `lower`, `upper`.
- **Validators**: `is_positive`, `is_non_negative`, `is_file`, `is_dir`, `is_int`, `is_str`.

### Data Science Pipelines (`data` kind)
- **Numpy**: `to_numpy`, `has_ndim(n)`, `is_shape(shape)`, `is_dtype(dtype)`.
- **Pandas**: `to_dataframe`, `has_columns(list)`, `min_rows(n)`.

### Physical Quantities (PyUnitWizard)
- Use factory functions from `argdigest.contrib.pyunitwizard_support`:
    - `check(dimensionality=...)`
    - `standardize()`
    - `convert(to_unit=...)`

## 4. Native Integrations
- **Pydantic**: You can pass `BaseModel` classes directly as rules in `@digest.map`.
- **Beartype**: Use `type_check=True` in the decorator to enforce type hints after digestion.

---
*Generated automatically by ArgDigest CLI. Do not edit manually unless necessary.*
