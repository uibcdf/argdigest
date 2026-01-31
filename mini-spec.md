# Mini-spec: ArgDigest argument-centric digestion (draft)

## 1) Objective and scope
- Implement an argument-centric digestion mode compatible with MolSysMT.
- Let each library define **where** and **how** digesters are discovered without imposing structure.
- Keep the core domain-agnostic and flexible.

## 2) Proposed public API
Decorator (new parameters):

```python
@digest(
    ...,  # existing args
    digestion_source=None,
    digestion_style="auto",
    standardizer=None,
    strictness="warn",
    skip_param="skip_digestion",
)
```

Parameters:
- `digestion_source`: `str | list[str]`
  - Module(s) or package(s) containing digesters.
- `digestion_style`: `"auto" | "registry" | "package" | "decorator"`
  - Discovery mode.
- `standardizer`: `callable | "module.path:function" | None`
  - Hook for argument-name normalization.
- `strictness`: `"warn" | "error" | "ignore"`
  - Behavior for arguments without a digester.
- `skip_param`: name of the bypass parameter.

## 3) Behavior contracts
- If `skip_param=True` in a call, **all digestion is skipped**.
- For each argument:
  - If a digester exists, run it and accept a transformed value.
  - If no digester exists:
    - `warn`: emit warning.
    - `error`: raise exception.
    - `ignore`: do nothing.
- After digestion, call the original function with digested values.

## 4) Digester discovery
- `registry`: look for `ARGUMENT_DIGESTERS` dict in `digestion_source`.
- `package`: scan a package and collect functions named `digest_<arg>`.
- `decorator`: use a global registry built by `@argument_digest`.
- `auto`: try in order `registry → package → decorator`, combining results with priority by the order of `digestion_source` entries.

## 5) Dependency resolution
- If a digester requires another argument by name, digest that argument first.
- Parameters can be injected from:
  - current argument values,
  - decorator parameters (like MolSysMT).
- Cycles raise a clear error listing the arguments involved.

## 6) Hooks and extensions
- `standardizer(caller, kwargs)` runs **before** digestion.
- It must return a dict with normalized argument names.

## 7) MolSysMT compatibility profile
- Expected usage:
  - `digestion_source="molsysmt._private.digestion.argument"`
  - `digestion_style="package"`
  - `standardizer="molsysmt._private.digestion.argument_names_standardization"`
  - `skip_param="skip_digestion"`
  - `strictness="warn"`

## 8) Acceptance criteria / tests
- Argument-specific digestion works and transforms values.
- Dependency resolution between arguments.
- `skip_digestion` bypasses all digestion.
- `standardizer` alters argument names based on caller.
- `strictness` enforces warn/error/ignore correctly.

---

## Near-term scope update (include B1)
- B1: Dual mode (argument-centric + kind pipelines) is included in the initial implementation plan.
- B2: Cache digestion plan per function remains future work.

## Out of scope for now (rest of B + C)
- B2: Cache digestion plan per function.
- B3: Execution auditing/profiling.
- B4: Automatic documentation of rules.
- C1: Declarative rule schemas (YAML/JSON).
- C2: Extra integrations (attrs/cattrs, numpy/pandas coercers).
