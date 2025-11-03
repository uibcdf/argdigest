from argdigest import digest, register_pipeline

@register_pipeline(kind="x", name="to-int")
def to_int(value, ctx):
    return int(value)

@digest(map={"a": {"kind": "x", "rules": ["to-int"]}})
def f(a, b):
    return a, b

def test_digest_basic():
    a, b = f("5", "x")
    assert a == 5
    assert b == "x"
