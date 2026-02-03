# Decorator design

The `@arg_digest` decorator can be configured for argument-centric digestion, pipelines, or both.

## Key parameters

- `digestion_source`: where to find digesters (module/package or list).
- `digestion_style`: discovery mode (`auto`, `registry`, `package`, `decorator`).
- `standardizer`: optional name-normalization hook.
- `strictness`: behavior for undigested arguments.
- `skip_param`: name of the bypass parameter.
- `map`: per-argument pipeline configuration.
- `config`: library-level defaults module or `DigestConfig`.

## Discovery styles

ArgDigest does not enforce a single layout. Libraries can choose the discovery style that
fits their architecture:

- `registry`: a module exposing `ARGUMENT_DIGESTERS = {"arg": fn, ...}`.
- `package`: a package containing functions named `digest_<argument>`.
- `decorator`: registration via `@argument_digest("arg")` anywhere in the codebase.
- `auto`: combine the above in a default order.

## Library-level defaults

To reduce repetition, a library can define defaults in `mylib/_argdigest.py` and pass
`config="mylib._argdigest"` to `@arg_digest`. The module can define:

- `DIGESTION_SOURCE`
- `DIGESTION_STYLE`
- `STANDARDIZER`
- `STRICTNESS`
- `SKIP_PARAM`

If `@arg_digest()` is used with no explicit config or overrides, ArgDigest will try to load
`<root_package>._argdigest` automatically based on the decorated function's module.

## Dual mode

When both argument digestion and pipelines are configured:

1) Arguments are digested first.
2) Pipelines run on the updated values.
