# Pipeline Design Patterns

Use pipelines for reusable rules shared across functions or argument families.

## Rule shape

```python
@register_pipeline(kind="feature", name="feature.base")
def feature_base(value, ctx):
    ...
    return value
```

The important part is not only the signature, but the behavioral contract:
inputs and outputs should be explicit, behavior should be deterministic, and
failures should be actionable. A rule should feel predictable to anyone reading
it in isolation.

## Context usage (`ctx`)

Use `ctx` for call-level context (function/argument metadata) when rule behavior
needs controlled context awareness.

In practice, `ctx` lets you write context-aware rules without relying on global
mutable state. That is a key point for maintainability: when behavior depends on
runtime context, make that dependency visible through `ctx`.

## Composition strategy

Prefer small composable rules over monolithic validators. Explicit rule lists
are easier to review, test, and evolve. Splitting coercion and validation also
helps because each step has one job and clearer failure semantics.

## Error strategy

When a rule fails, the message should tell users what was wrong and what to do
next. Include argument identity and concrete constraints in the error whenever
possible. Specific exceptions are also better than generic failures because they
make downstream handling and test assertions clearer.

## Anti-patterns

Some anti-patterns are common and expensive: mutating unrelated arguments,
depending on import-time side effects, and silently swallowing invalid input.
These patterns make behavior hard to reason about and usually create subtle
regressions later.

## Next

Continue with [Strictness and Errors](strictness-and-errors.md).
