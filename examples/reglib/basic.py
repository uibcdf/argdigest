"""Example functions using registry-style argument digesters."""

from argdigest import arg_digest, register_pipeline


@register_pipeline(kind="scalar", name="double")
def double(value, ctx):
    return value * 2


@arg_digest(config="reglib._argdigest", map={"a": {"kind": "scalar", "rules": ["double"]}})
def analyze(a, b, skip_digestion=False):
    return a, b
