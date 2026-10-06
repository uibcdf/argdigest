# Release notes

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
