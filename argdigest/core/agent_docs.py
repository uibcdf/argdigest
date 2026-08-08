"""
Logic for generating and updating AI Agent instructions based on library configuration.
"""
from __future__ import annotations
import os
import importlib
from .config import resolve_config
from .function_contract import describe_contract
from .function_loader import load_domains, load_function_contracts, load_normalization
from .normalization import describe_normalization


def _hashable(source):
    """lru_cache keys must be hashable; a list of sources becomes a tuple."""

    return tuple(source) if isinstance(source, list) else source


def _render_normalization(registry) -> str:
    """Render the declared aliases so an agent can see what names already exist."""

    if registry is None:
        return "_Alias declarations could not be loaded._"
    described = describe_normalization(registry)
    if not described:
        return ("_No alias declared. Users must type the canonical argument names "
                "exactly._")

    lines = ["| Applies to | When | Aliases |", "| --- | --- | ---: |"]
    for entry in described:
        when = "" if entry["when"] is None else ", ".join(
            f"{k}={v!r}" for k, v in entry["when"].items())
        lines.append(f"| `{entry['applies_to']}` | {when} | {len(entry['aliases'])} |")
    return "\n".join(lines)


def _render_axis_one(contracts, domains) -> str:
    """Render the declared contracts and domains as a table an agent can read."""

    if contracts is None:
        return "_Axis 1 declarations could not be loaded._"

    lines = []
    if domains:
        lines.append("**Declared domains**\n")
        lines.append("| Domain | Members | Description |")
        lines.append("| --- | ---: | --- |")
        for name, domain in sorted(domains.items()):
            members = domain.known_members()
            size = str(len(members)) if members else "not enumerable"
            lines.append(f"| `{name}` | {size} | {domain.description or ''} |")
        lines.append("")

    declared = contracts.declared_callers()
    if declared:
        lines.append("**Declared function contracts**\n")
        lines.append("| Caller | Admits | Requires |")
        lines.append("| --- | --- | --- |")
        for key in declared:
            contract = contracts.resolve(key) or contracts._exact.get(key)
            if contract is None:
                continue
            described = describe_contract(contract, domains)
            requires = described["requires_any_of"] or ""
            lines.append(f"| `{key}` | `{described['admits']}` | {requires} |")
        lines.append("")

    if not lines:
        return ("_No function contract declared. Every closed signature is still held to "
                "its own parameters; functions taking `**kwargs` admit anything._")
    return "\n".join(lines)


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

    # Axis 1 declarations, rendered as data. This is what makes the accepted domain of a
    # `**kwargs` function visible: `inspect.signature` cannot show it.
    try:
        contracts = load_function_contracts(_hashable(cfg.function_source))
        domains = load_domains(_hashable(cfg.domain_source))
        normalization = load_normalization(_hashable(cfg.normalization_source))
    except Exception:
        contracts, domains, normalization = None, {}, None

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

### Axis 1 -- the function argument contract
- **Function Source**: `{cfg.function_source}`
- **Domain Source**: `{cfg.domain_source}`
- **Unknown Argument Policy**: `{cfg.unknown_argument}`

{_render_axis_one(contracts, domains)}

### Declared argument-name aliases
- **Normalization Source**: `{cfg.normalization_source}`

{_render_normalization(normalization)}

## 2. Your Mission as an Agent
Whenever you modify or add a function in this library:
1. **Apply Digestion**: Ensure the function is decorated with `@arg_digest()`.
2. **Check Arguments**: If you add new arguments, check if they need a specific digester in the `digestion_source` directory.
2a. **Declare aliases**: if users are likely to type another name for an argument, add an `AliasTable` in `normalization_source` rather than renaming by hand. Aliases are applied before the contract, so they never conflict with it.
2b. **Declare the contract**: if the function takes `**kwargs`, declare in `function_source` which domain those keywords come from. Left undeclared, the function accepts anything, which is the defect axis 1 exists to prevent. A closed signature needs no declaration: it is held to its own parameters.
3. **Use Pipelines**: For specific validation (e.g. ranges, types), use `arg_digest.map` with appropriate rules.
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
- **Pydantic**: You can pass `BaseModel` classes directly as rules in `arg_digest.map`.
- **Beartype**: Use `type_check=True` in the decorator to enforce type hints after digestion.

---
*Generated automatically by ArgDigest CLI. Do not edit manually unless necessary.*
"""
    with open(output_file, "w") as f:
        f.write(content)
    
    return os.path.abspath(output_file)