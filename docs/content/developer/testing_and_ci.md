# Testing and CI

Run tests with pytest:

```bash
pytest
```

## Recommended local gate sequence

Before opening a PR, run this sequence:

```bash
pytest
cd docs && make html
```

If your change touches examples or integration behavior, also run at least one
manual smoke path from `examples/` to verify end-to-end decorator behavior.

## Coverage expectations

- New runtime behavior must include direct tests.
- Integration-facing behavior should include smoke-level tests.
- Error/warning behavior must be validated explicitly.

## Documentation checks

When docs are modified, validate that:
- toctree references resolve correctly,
- code snippets reflect the current API,
- migration guidance is still coherent.

## Environment

Use the development conda environment in `devtools/` to keep local and CI
behavior aligned.

## CI pass criteria

A contribution is considered CI-ready when:
- tests are green,
- docs build succeeds,
- no public-contract behavior changed without docs/tests updates.
