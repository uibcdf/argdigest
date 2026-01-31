# What is ArgDigest?

**ArgDigest** is a lightweight, extensible library to audit, normalize, and validate function
arguments in scientific Python libraries.

It provides two complementary mechanisms:

- **Argument-centric digestion**: per-argument digesters that validate or coerce values.
- **Pipeline-based validation**: reusable rules grouped by `kind` and executed in order.

ArgDigest is domain-agnostic by design. Each library provides its own digestion logic while
ArgDigest supplies the execution engine, error model, and optional discovery utilities.
