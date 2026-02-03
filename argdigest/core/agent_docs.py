"""
Logic for generating and updating AI Agent instructions based on library configuration.
"""
from __future__ import annotations
import os
import importlib
from .config import resolve_config

def generate_agent_docs(module_name: str, output_file: str = "ARG_DIGEST_AGENTS.md"):
    """
    Detects library config and writes the ARG_DIGEST_AGENTS.md file.
    """
    try:
        importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(f"Could not import module '{module_name}' to detect configuration: {e}")

    # Try to resolve config for this module
    # We use the same auto-discovery logic as the decorator
    try:
        import_module_path = f"{module_name}._argdigest"
        cfg = resolve_config(import_module_path)
    except Exception:
        # Fallback to current global defaults if _argdigest.py is missing
        from .config import get_defaults
        cfg = get_defaults()

    content = f"""# ArgDigest Agent Instructions for {module_name}

This document provides context and instructions for AI Agents (like yourself) to maintain and use **ArgDigest** within this project.

## 1. Project Context
- **Library Module**: `{module_name}`
- **Digestion Style**: `{cfg.digestion_style}`
- **Digestion Source**: `{cfg.digestion_source}`
- **Standardizer**: `{cfg.standardizer}`
- **Strictness Level**: `{cfg.strictness}`
- **Bypass Parameter**: `{cfg.skip_param}`
- **PUW Context**: `{cfg.puw_context}`

## 2. Your Mission as an Agent
Whenever you modify or add a function in this library:
1. **Apply Digestion**: Ensure the function is decorated with `@argdigest.digest()`.
2. **Check Arguments**: If you add new arguments, check if they need a specific digester in the `digestion_source` directory.
3. **Use Pipelines**: For specific validation (e.g. ranges, types), use `@arg_arg_digest.map` with appropriate rules.
4. **Maintenance**: If you change the ArgDigest configuration (e.g. adding a standardizer), you **MUST** run `argdigest agent update --module {module_name}` to keep this file in sync.

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
- **Pydantic**: You can pass `BaseModel` classes directly as rules in `@arg_arg_digest.map`.
- **Beartype**: Use `type_check=True` in the decorator to enforce type hints after digestion.

---
*Generated automatically by ArgDigest CLI. Do not edit manually unless necessary.*
"""
    with open(output_file, "w") as f:
        f.write(content)
    
    return os.path.abspath(output_file)