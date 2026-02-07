import pytest
from argdigest import arg_digest, register_pipeline
from argdigest.core.config import DigestConfig

# Use a concrete config to avoid auto-discovery of tests._argdigest
cfg_decorator = DigestConfig(digestion_style="decorator", strictness="ignore")

def test_explicit_map_digestion():
    @register_pipeline(kind="x", name="to-int")
    def to_int(v, ctx):
        return int(v)

    @arg_digest(map={"a": {"kind": "x", "rules": ["to-int"]}}, config=cfg_decorator)
    def f(a):
        return a

    assert f("10") == 10


def test_implicit_kind_digestion():
    @register_pipeline(kind="y", name="to-float")
    def to_float(v, ctx):
        return float(v)

    @arg_digest(kind="y", rules=["to-float"], config=cfg_decorator)
    def f(a, b):
        return a, b

    a, b = f("1.5", "2.5")
    assert a == 1.5
    assert b == 2.5


def test_map_overrides_default_kind():
    @register_pipeline(kind="z", name="plus-one")
    def plus_one(v, ctx):
        return v + 1

    @register_pipeline(kind="w", name="minus-one")
    def minus_one(v, ctx):
        return v - 1

    @arg_digest(kind="z", rules=["plus-one"], map={"b": {"kind": "w", "rules": ["minus-one"]}}, config=cfg_decorator)
    def f(a, b):
        return a, b

    a, b = f(10, 10)
    assert a == 11
    assert b == 9
