import pytest
from argdigest import arg_digest, register_pipeline

@register_pipeline(kind="int", name="convert")
def to_int(value, ctx):
    return int(value)

def test_beartype_native_integration():
    # Use native type_check parameter
    arg_digest.map(type_check=True, a={"kind": "int", "rules": ["convert"]})
    def f(a: int):
        return a

    # Valid digestion + valid type check
    assert f("42") == 42

    # Invalid type check (if digestion produced wrong type, beartype would catch it)
    # But here digestion works. Let's try undigested argument.
    
    @arg_digest(type_check=True) # strictness=warn by default
    def g(a: int):
        return a
        
    # 'a' is not digested, so it remains string. Beartype should raise error.
    from beartype.roar import BeartypeCallHintParamViolation
    with pytest.raises(BeartypeCallHintParamViolation):
        g("42")