# Release notes

## 0.17.0

`DigestConfig.contract_owner` optionally fixes contract lookup independently of
runtime diagnostic identity. `None` preserves existing resolution;
`"definition"` uses each decorated function's defining `module.function`;
an exact dotted key selects a logical owner. The selected key drives aliases,
standardizers, function/domain contracts and digester `caller`. Bound methods
retain their runtime class in `qualname`. Configuration loaders, both decorator
forms, digestion plans and CLI audit support the option. Supply it through
configuration: a decorator keyword named `contract_owner` keeps its existing
meaning as arbitrary digester context.

Alias normalization preserves canonical supplied names for required,
co-required and exclusive rules, including aliases on closed signatures.
Variadic positional arguments no longer make omitted keyword-only defaults
appear supplied. Staticmethod descriptors are preserved in both decorator
orders, for access through class and instance.

Python 3.11–3.14 and core dependency floors remain unchanged. The exact noarch
package passed full installed qualification and a separate NumPy-free lower-bound
matrix before same-file public promotion. Consumer adoption remains independently owned.

## 0.16.0

With SMonitor 0.20.0 or newer, importing ArgDigest registers its diagnostic
catalog without configuring application policy, handlers or exception hooks.
The public `register_diagnostics()` helper exposes this idempotent operation.
`configure_diagnostics()` preserves existing application configuration by
default; `use_provider_policy=True` explicitly requests provider recommendations
when supported. The CLI configures its own diagnostic session.

Optional type-check engine loading is deferred until use. Older supported
providers retain legacy initialization and reject explicit registration-only
requests with an actionable capability error. Python 3.11–3.14 and the core
dependency floors remain unchanged.

The staged release requires full installed qualification with public SMonitor
0.21.0 and DepDigest 0.15.1 and a separate NumPy-free lower-bound matrix before
exact-file promotion. Consumer adoption remains independently owned.

## 0.15.0

`capture_policy="metadata_only"` delegates diagnostic collection restrictions
to SMonitor before ArgDigest instrumentation and formatting. Values and native
error text are omitted from library telemetry, while contracts, normalization,
pipelines and native failure behavior remain active. Nested scopes cannot relax
an enclosing restriction. Scoped capture requires public SMonitor 0.19.0 or a
compatible newer version; older providers reject an explicit restrictive
request. Detailed defaults and the core dependency floors remain unchanged.

`argument_digestion=None/True/False` selects argument digesters independently
of configuration. `None` preserves historical inference, `True` retains strict
missing-digester checks, and `False` selects pipelines while retaining signature
binding, function/domain contracts, aliases, standardization and type checks.
Both decorator forms, configuration loaders, plans and CLI audit support it.

The noarch package is qualified using the complete installed suite with public
SMonitor 0.19.0 and a separate NumPy-free lower-bound compatibility matrix on
Linux, macOS ARM64 and Windows with Python 3.11–3.14 before promotion. Consumer
adoption remains independent of this provider release.

## 0.14.0

NumPy is now optional for basic installation. Scientific consumers should
declare NumPy directly or install the `science` extra from source. The
`pyunitwizard` extra includes NumPy and PyUnitWizard.

Only literal `skip_digestion=True` bypasses validation. Replace truthy strings
or integers with an explicit boolean when bypass is intended.

Classmethods work in both decorator orders without digesting their `cls`
receiver. Digesters can accept optional `qualname` to identify the runtime
class-qualified method; existing `caller` registry keys are preserved.
Contract refusals show the cause and allowed arguments more clearly.

PyUnitWizard adapter and factory creation defer importing the provider until
an operation runs. Missing-provider diagnostics and original transitive import
exceptions are preserved. Python 3.11–3.14 and core dependency floors remain
unchanged.
