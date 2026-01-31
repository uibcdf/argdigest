import pytest
from argdigest import digest, DigestValueError

def test_std_coercers():
    @digest.map(
        flag={"kind": "std", "rules": ["to_bool"]},
        items={"kind": "std", "rules": ["to_list"]},
        text={"kind": "std", "rules": ["strip", "upper"]}
    )
    def process(flag, items, text):
        return flag, items, text

    f, i, t = process("yes", "scalar", "  hello  ")
    assert f is True
    assert i == ["scalar"]
    assert t == "HELLO"

def test_std_validators():
    @digest.map(num={"kind": "std", "rules": ["is_positive"]})
    def calc(num):
        return num

    assert calc(10) == 10
    
    with pytest.raises(DigestValueError):
        calc(-5)
