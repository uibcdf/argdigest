# FAQ

## Do I need to use `package` style?

No. ArgDigest supports `package`, `registry`, `decorator`, and `auto` styles.
Choose the one that fits your library architecture.

## Should I always define `_argdigest.py`?

It is strongly recommended. It centralizes defaults and avoids repeating
decorator arguments throughout the codebase.

## Do I have to declare a contract for every function?

No. A closed signature already declares its own domain, so ArgDigest holds it to its own
parameters with no declaration at all. Only a function taking `**kwargs` needs one: it
opened its door deliberately and ArgDigest cannot guess what it meant, so it admits
anything until you say otherwise.

## Why does a typo now raise instead of being ignored?

Because the alternative is worse. A discarded keyword means the call runs with the
default and returns a well-formed, wrong answer, and nothing in the result reveals it.
ArgDigest also should never end up more permissive than Python, which already raises
`TypeError` for an unexpected keyword. Set `UNKNOWN_ARGUMENT = "warn"` while migrating an
existing codebase.

## My function legitimately takes many keywords. Must I list them all?

No — declare a `Domain` pointing at whatever already defines them in your library. If the
names live in a catalogue, the domain reads that catalogue, so the two cannot drift
apart. It also makes those names readable from outside, which `inspect.signature` cannot
show.

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
