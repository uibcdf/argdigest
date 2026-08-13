# Decorator design

The `@arg_digest` decorator can be configured for argument-centric digestion, pipelines, or both.

## Key parameters

- `digestion_source`: where to find digesters (module/package or list).
- `digestion_style`: discovery mode (`auto`, `registry`, `package`, `decorator`).
- `normalization_source`: where to find declared alias tables.
- `standardizer`: optional name-normalization hook, for renames a table cannot state.
- `strictness`: behavior for undigested arguments.
- `function_source` / `domain_source`: where to find function contracts and named domains.
- `unknown_argument`: behavior for a keyword outside a function's contract.
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
- `NORMALIZATION_SOURCE`
- `FUNCTION_SOURCE`
- `DOMAIN_SOURCE`
- `UNKNOWN_ARGUMENT`

If `@arg_digest()` is used with no explicit config or overrides, ArgDigest will try to load
`<root_package>._argdigest` automatically based on the decorated function's module.

## The stages of a call

```
bind_arguments -> normalization -> standardizer -> function contract -> digestion
```

The order is forced by dependencies, not chosen for convenience.

**Normalization and the standardizer come first** so that a keyword is canonical before
anything judges it. If the contract ran first it would reject every alias a library
declares as an unknown argument.

**The function contract comes before digestion** because validating the value of an
argument that should not be there is wasted work ending in a confusing failure.

`bind_arguments` sets aside the keywords a closed signature cannot take and hands them to
the contract stage rather than discarding them. A binding step must not make a policy
decision — that it did was the defect the function contract was introduced to repair.

## Dual mode

When both argument digestion and pipelines are configured:

1) Arguments are digested first.
2) Pipelines run on the updated values.
