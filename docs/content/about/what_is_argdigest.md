# What is ArgDigest?

**ArgDigest** is a lightweight, extensible library to audit, normalize, and validate function
arguments in scientific Python libraries.

It covers **two axes** of the same problem:

- **The function argument contract**: which keywords a function may receive, which it
  requires, and which exclude each other. Declared as `FunctionContract` and `Domain`.
- **The argument value contract**: whether a given argument's value is valid and in
  canonical form. Declared as per-argument digesters, optionally composed with
  **pipeline rules** — reusable checks grouped by `kind` and executed in order.

Without the first, a mistyped keyword is discarded in silence: the call runs with the
default and returns a plausible wrong answer, which in a scientific library is the worst
failure mode there is, because nothing in the result looks wrong.

ArgDigest is domain-agnostic by design. Each library provides its own digestion logic while
ArgDigest supplies the execution engine, error model, and optional discovery utilities.
