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
    
def test_load_from_package_mock(tmp_path, monkeypatch):
    # Create a mock package
    pkg_dir = tmp_path / "mock_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    mod_dir = pkg_dir / "arg_mod.py"
    mod_dir.write_text("def digest_test_arg(test_arg, caller=None): return test_arg")
    
    import sys
    monkeypatch.syspath_prepend(str(tmp_path))
    
def test_load_from_registry_not_dict(tmp_path, monkeypatch):
    pkg_dir = tmp_path / "bad_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("ARGUMENT_DIGESTERS = 'not a dict'")
    
    import sys
    monkeypatch.syspath_prepend(str(tmp_path))
    from argdigest.core.argument_loader import load_argument_digesters
    with pytest.raises(TypeError, match="must be a dict"):
        load_argument_digesters("bad_pkg", "registry")
