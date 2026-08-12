# Proposal: Automated Type-Stub Generator (`argdigest build-stubs`)

> **Kept, scheduled post-1.0 (2026-08-12).** It became more feasible than when it was
> written: axis 1 already solved the hard half. `describe_contract()` renders the
> accepted domain of a `**kwargs` function as plain data — precisely what
> `inspect.signature` cannot see and what a stub generator needs. What is still missing
> is annotations on the digesters themselves, which nothing currently requires.
>
> One correction for whoever picks this up: the proposal says the digestion directory is
> `_private/arg_digestion/`. The convention is `_private/argdigest/argument/`.

## Abstract

We propose introducing an automated, offline type-stub generator (`argdigest build-stubs`) to `argdigest`. This tool will parse a library's central digestion directory (`_private/arg_digestion/`) and dynamically compile PEP 484-compliant static type stub files (`.pyi`). 

This solves the long-standing "Zero-Intrusion Typing" dilemma in scientific Python code: enabling full static type checking and autocomplete in IDEs (like Pyright, mypy, and VSCode) without bloating implementation code with type annotations or manual castings.

---

## The Problem

Under UIBCDF guidelines, `argdigest` is highly valued for keeping scientific codebases clean and standard. Developers write plain Python code, and `argdigest` automatically sanitizes, validates, and coerces arguments based on definitions in `_private/arg_digestion/`.

However, static type checkers (Pyright/mypy) run offline without importing modules. Consequently:
1. They are blind to the runtime coercion performed by `@arg_digest`.
2. Inside a function (e.g., `add_sphere(self, center, radius)`), the IDE treats `center` as `Any` or its flexible raw input types (e.g., `Union[list, tuple]`), triggering typing errors when accessing canonical methods (like `.astype()`).
3. If the developer types the input parameter as the canonical type (`np.ndarray`), users receive typing warnings in notebooks when passing a common Python list.

Adding annotations directly in the `.py` files using `Annotated` or `Union` inflates the method signatures, degrading code legibility.

---

## Proposed Solution

Introduce an offline compiler CLI command:
```bash
argdigest build-stubs [target_directory]
```

### 1. Extraction Pipeline
The stub generator will:
* Inspect all functions decorated with `@arg_digest`.
* For each parameter (e.g., `center`), it will map it to its corresponding digestion definition script in `_private/arg_digestion/argument/center.py`.
* Statically parse the digester function's signature and annotations to extract:
  * **Allowed Input Types**: E.g., `Union[list, tuple, np.ndarray, Quantity]`.
  * **Returned Canonical Type**: E.g., `np.ndarray` of `float64`.

### 2. Stub Compilation (`.pyi`)
It will write a companion `.pyi` stub file next to the source `.py` files.
In the generated `.pyi` file:
* The public function signature will be annotated with the **flexible input types** to ensure external users get autocomplete and see valid parameters.
* This keeps the `.py` source file completely untouched, elegant, and standard.

### 3. Developer Tooling Watcher
To avoid requiring developers to run this manually:
* Support a `--watch` mode that runs a fast background file-system watcher.
* Provide standard VSCode task recipes (`.vscode/tasks.json`) in the templates so that saving a `.py` file automatically regenerates stubs in <50ms.
* Enable dynamic verification in CI pipelines to prevent committing out-of-sync stubs.

---

## Performance & Impact

* **Runtime Performance**: **Zero-cost**. The stub generation is entirely offline or design-time. The end-user in production runs the clean `.py` file directly, incurring absolutely no CPU overhead.
* **Typing Auditability**: Enables running `mypy` or `pyright` in CLI and CI/CD pipelines to verify the library's type-safety without writing a single type annotation in scientific source files.
