import pytest
from argdigest import digest
from argdigest.pipelines.coercers import to_tuple

def test_to_tuple_coercer():
    @digest.map(v={"kind": "std", "rules": ["to_tuple"]})
    def f(v): return v
    
    assert f("a") == ("a",)
    assert f([1, 2]) == (1, 2)
    assert f((3, 4)) == (3, 4)
    # Generic iterable (range)
    assert f(range(2)) == (0, 1)

def test_argument_loader_errors():
    from argdigest.core.argument_loader import load_argument_digesters
    # style not auto
    with pytest.raises(ValueError, match="digestion_style must be"):
        load_argument_digesters("source", "invalid_style")
    
    # Load from missing registry
    # This should return empty dict or raise error depending on implementation
    # Current implementation imports module and looks for ARGUMENT_DIGESTERS
    with pytest.raises(ImportError):
        load_argument_digesters("non_existent_module", "registry")

def test_standardizer_resolver_errors():
    from argdigest.core.argument_loader import resolve_standardizer
    with pytest.raises(ValueError, match="standardizer must be"):
        resolve_standardizer("module_without_colon_or_dot")
    
    with pytest.raises(TypeError):
        resolve_standardizer(123)
