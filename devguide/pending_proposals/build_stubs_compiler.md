---
summary: Generate offline type stubs from ArgDigest contracts after 1.0.
issue: uibcdf/argdigest#9
status: open
opened: 2026-09-07
closed:
verification: inspected
area: [typing, tooling]
guard:
normative:
blocked_by: []
supersedes: []
---

# Proposal: Automated Type-Stub Generator (`argdigest build-stubs`)

> **Kept, scheduled post-1.0 (2026-08-12).** It became more feasible than when it was
> written: axis 1 already solved the hard half. `describe_contract()` renders the
> accepted domain of a `**kwargs` function as plain data — precisely what
> `inspect.signature` cannot see and what a stub generator needs. What is still missing
> is annotations on the digesters themselves, which nothing currently requires.
>
> One correction for whoever picks this up: the proposal says the digestion directory is
> `_private/arg_digestion/`. The convention is `_private/argdigest/argument/`.

## Reassessment — 2026-10-22

The maintainer requested a reassessment after `uibcdf/argdigest#37`. The
recommendation is to advance a small feasibility pilot, rather than the full
compiler/watch service. The full generator remains scheduled after 1.0 until
the pilot establishes a useful, accurate type source. No pilot or generator is
implemented by this reassessment.

A static AST inspection of the clean MolSysMT argument-digester directory at
`55f04ebfe364c1918a912e2d76aee8db95959dde` found 461 top-level `digest_*`
functions: zero annotate their value input and zero annotate their return.
460 read `caller` in their bodies; that syntactic count includes forwarding
and does not mean every result type depends on the caller. The existing
`n_atoms` digester demonstrates context-dependent acceptance rules. This is
evidence for one concrete consumer, not an audit of every suite member.

There are three distinct type questions:

1. Which input types may users pass to the decorated function?
2. Which canonical type reaches its implementation after digestion?
3. What does the decorated function itself return?

The return annotation of a value digester can inform question 2; it cannot
determine question 3. The original proposal's promise of checking an otherwise
unannotated scientific implementation solely through companion stubs is too
broad. Stubs describe the interface that users import; they do not themselves
teach a type checker that a runtime decorator changed local parameter types.
See the primary [stub specification](https://typing.python.org/en/latest/spec/distributing.html)
and [mypy stub documentation](https://mypy.readthedocs.io/en/stable/stubs.html).

`describe_contract()` helps enumerate declared keyword interfaces, but it is a
runtime operation. A strictly offline compiler cannot generally execute
consumer imports, arbitrary domain predicates, standardizers or pipeline
factories. A pilot must define its supported input declarations and report
unknowns, rather than infer scientific types from argument names. Existing
stub generators can provide scaffolding; the useful ArgDigest contribution
would be trustworthy contract-derived information. See the primary
[stub-writing guide](https://typing.python.org/en/latest/guides/writing_stubs.html).

Proposed pilot acceptance:

- Use 3–5 representative digesters, including simple normalization, a scientific
  value and caller-dependent behavior; explicitly declare accepted/canonical
  types and preserve the public function's own return contract separately.
- Choose whether declarations use annotations or a separate static schema;
  require an explicit representation for contextual alternatives.
- Demonstrate useful consumer signatures with a real type checker: valid calls
  pass and invalid calls fail. Assess implementation-body checking separately.
- Cover inheritance/explicit contract ownership from #37, aliases and unknown
  contracts; emit explicit incomplete types when information is unavailable.
- Generate a reviewed preview into a separate output directory. Measure the
  benefit and required manual declarations before expanding scope.

Watcher integration, automatic adjacent `.pyi` writes and the original
unmeasured sub-50-ms target are deferred. Advancing the complete original scope
now would front-load tooling before the necessary type information exists.

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
