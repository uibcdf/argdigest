import pytest
from argdigest.contrib.beartype_support import beartype_digest
from argdigest.contrib.pydantic_support import model_from_dict
from pydantic import BaseModel

def test_legacy_beartype_digest():
    @beartype_digest(map={"a": {"kind": "std", "rules": ["is_int"]}})
    def f(a: int):
        return a
    
    assert f(10) == 10
    # ArgDigest catches the error first
    from argdigest import DigestTypeError
    with pytest.raises(DigestTypeError):
        f("not_int")

def test_contrib_pydantic_pipeline():
    from argdigest.contrib.pydantic_support import pydantic_pipeline
    class Data(BaseModel):
        x: int
    
    pipe = pydantic_pipeline(Data)
    # Valid
    res = pipe({"x": 1}, None)
    assert res.x == 1
    # Invalid
    with pytest.raises(ValueError, match="Pydantic validation failed"):
        pipe({"x": "nan"}, None)

def test_pydantic_helper_model_from_dict():
    class User(BaseModel):
        name: str
    
    # Already instance
    u1 = User(name="Diego")
    assert model_from_dict(User, u1) is u1
    
    # From dict
    u2 = model_from_dict(User, {"name": "Diego"})
    assert u2.name == "Diego"
    
    # Fail
    with pytest.raises(TypeError):
        model_from_dict(User, 123)
