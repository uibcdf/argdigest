import pytest
from argdigest import arg_digest

def test_to_tuple_coercer():
    @arg_digest.map(v={"kind": "std", "rules": ["to_tuple"]})
    def f(v): return v
    
    assert f("a") == ("a",)
    assert f([1, 2]) == (1, 2)