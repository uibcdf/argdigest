from argdigest import arg_digest, register_pipeline

@register_pipeline(kind="x", name="to-int")
def to_int(value, ctx):
    return int(value)

@arg_digest(map={"a": {"kind": "x", "rules": ["to-int"]}})
def f(a, b):
    return a, b

def test_digest_basic():
    a, b = f("5", "x")
    assert a == 5
    assert b == "x"


def test_digest_all_arguments_implicit_map():
    """Test that kind/rules apply to all arguments if map is not provided."""
    @arg_digest(kind="x", rules=["to-int"])
    def g(a, b):
        return a, b
    
    # Both arguments should be converted to int
    val_a, val_b = g("10", "20")
    assert val_a == 10
    assert val_b == 20


def test_digest_map_alias():
    """Test the @arg_arg_digest.map alias syntax."""
    @arg_arg_digest.map(a={"kind": "x", "rules": ["to-int"]})
    def h(a, b):
        return a, b
    
    val_a, val_b = h("99", "y")
    assert val_a == 99
    assert val_b == "y"