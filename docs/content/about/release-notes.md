# Release notes

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
