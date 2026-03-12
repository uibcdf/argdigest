# ArgDigest Developer Guide

## 1. Introduction

ArgDigest is a toolkit for enforcing input argument consistency in scientific Python libraries.
It combines argument-centric digestion with reusable pipeline-based validation.

## 2. Core Concepts

### 2.1 `@arg_digest` decorator

`@arg_digest` can execute two validation layers:

- Argument digesters discovered by name (`package`, `registry`, `decorator`, or `auto` styles).
- Pipelines registered by `kind` and `rules`.

If both layers are configured, argument digestion runs first, then pipelines run on transformed values.

### 2.2 Explicit mapping

Use `arg_digest.map` for per-argument pipeline rules:

```python
from argdigest import arg_digest

arg_digest.map(
    feature={"kind": "feature", "rules": ["feature.base", "feature.shape"]},
    parent={"kind": "feature", "rules": ["feature.base"]},
)
def link(feature, parent):
    ...
```

### 2.3 Configuration resolution

ArgDigest supports four configuration modes:

1. Explicit decorator arguments (`digestion_source`, `digestion_style`, etc.).
2. Explicit config module (`config="my_lib._argdigest"`).
3. Environment config module (`ARGDIGEST_CONFIG="my_lib._argdigest"`).
4. Auto-discovery of `<root_package>._argdigest` when no explicit config/overrides are passed.

## 3. Error and Diagnostics Model

ArgDigest exceptions and warnings are catalog-backed and include context/hints.
Main classes are exposed from `argdigest.core.errors`.

Diagnostics stack:

- `argdigest/_smonitor.py` for runtime profile.
- `argdigest/_private/smonitor/catalog.py` for codes/signals.
- `argdigest/_private/smonitor/meta.py` for URLs and hint metadata.

Instrumentation:

- Digestion wrapper uses `@smonitor.signal`.
- `Registry.run` uses `@smonitor.signal(tags=["pipeline"])`.

## 4. Configuration and CLI

### 4.1 Configuration loading

```python
from argdigest.config import load_from_file
cfg = load_from_file("my_config.yaml")
```

Supported formats: `.py`, `.yaml/.yml`, `.json`.

### 4.2 CLI commands

```bash
argdigest audit my_lib.api
argdigest health-check
argdigest agent init --module my_lib
argdigest agent update --module my_lib
```

## 5. QA Checklist (Before Release)

1. Tests:

```bash
pytest
```

2. Lint:

```bash
ruff check .
```

3. Install + CLI sanity:

```bash
pip install -e .
argdigest --help
```

Release quality rule: tests and lint must both pass.

## 6. Packaging Rules

- Use setuptools package discovery for releases:

```toml
[tool.setuptools.packages.find]
include = ["argdigest*"]
```

- Do not replace this with a single-package list (for example `packages = ["argdigest"]`),
  because that excludes subpackages such as `argdigest._private`, `argdigest.core`,
  and `argdigest.pipelines` from wheels.
- Always validate wheel contents when changing packaging settings.

## 7. CI Workflow Guardrails

- The import smoke-check steps in CI/docs workflows must fail hard on import errors.
- Keep `set -euo pipefail` in import-check run blocks.
- Keep import checks running from outside the repository root (`cd` to home)
  so they validate installed wheel behavior, not local source-tree fallback.

## 8. Minimal Example

```python
from pydantic import BaseModel
from argdigest import arg_digest

class Feature(BaseModel):
    feature_id: str
    shape_type: str

arg_digest.map(
    feature={"kind": "feature", "rules": [Feature]},
    type_check=True,
)
def register_feature(feature: Feature):
    return feature.feature_id
```

## 9. Current Focus

- Consolidate `0.9.x` as final RC before `1.0.0`.
- Keep docs/examples aligned with runtime behavior.
- Validate remote release gates and downstream integration stability.
- Keep shared collective E2E baseline green (`tests/e2e/test_collective_error_path.py`) during RC consolidation.

## 🥇 MolSysSuite Integration (March 2026 Updates)

### Scientific Coercers
The `sci` kind has been added to provide standardized normalization for scientific data types using `pyunitwizard`:
- `to_quantity_array`: Standardizes input to a numpy array, optionally converting units.
- `to_float64_array`: Shortcut for float64 precision (mandatory for Numba kernels).
- `to_int64_array`: Shortcut for int64 precision.

### Automatic Observability
The `@arg_digest` decorator now automatically reports failures to `smonitor` with code `MSM-DBG-PROBE-001` at `DEBUG` level. It also captures the original exception as the `cause`, providing deep traceability without manual boilerplate in the host library.
