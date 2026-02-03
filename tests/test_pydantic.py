import pytest
from argdigest import arg_digest

try:
    from pydantic import BaseModel
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False

if HAS_PYDANTIC:
    class User(BaseModel):
        name: str
        age: int

@pytest.mark.skipif(not HAS_PYDANTIC, reason="pydantic not installed")
def test_pydantic_native_integration():
    # Pass the Pydantic class DIRECTLY as a rule
    @arg_arg_digest.map(u={"kind": "data", "rules": [User]})
    def process_user(u):
        return u

    # Case 1: Dict input -> Model
    user = process_user({"name": "Diego", "age": 30})
    assert isinstance(user, User)
    assert user.name == "Diego"
    assert user.age == 30

    # Case 2: Invalid input -> Error
    with pytest.raises(ValueError, match="Validation failed"):
        process_user({"name": "Diego", "age": "not_an_int"})