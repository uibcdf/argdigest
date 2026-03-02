# FAQ

## Do I need to use `package` style?

No. ArgDigest supports `package`, `registry`, `decorator`, and `auto` styles.
Choose the one that fits your library architecture.

## Should I always define `_argdigest.py`?

It is strongly recommended. It centralizes defaults and avoids repeating
decorator arguments throughout the codebase.

## Can I combine digesters and pipelines?

Yes. Digestion runs first; pipelines run after digestion on updated values.

## What should I use first: `warn` or `error` strictness?

Use `warn` while migrating, then move to `error` when coverage is complete.

## Can ArgDigest replace custom digestion engines?

Yes, that is a core target. Adopt in phases and keep compatibility during
transition (`auto` style helps mixed migrations).

## Does ArgDigest force one folder layout?

No. The goal is contract-level consistency with architectural freedom.

## I am an end user of a host library. Do I need to install or configure ArgDigest directly?

Usually no. You interact with ArgDigest indirectly through the host library.
What matters for you is how to interpret validation messages and adjust input
according to that library's API.

## Why did an input that worked before start failing after update?

Many integrations move from permissive to strict validation over time. A warning
in older versions can become an error in newer versions when the contract is
hardened. Check release notes and migration guidance from the host library.
