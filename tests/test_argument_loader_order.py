from __future__ import annotations

from types import ModuleType, SimpleNamespace

from argdigest.core import argument_loader


def test_package_loader_sorts_modules_for_deterministic_order(monkeypatch):
    package = ModuleType("dummy_pkg")
    package.__path__ = ["dummy_path"]

    mod_b = ModuleType("dummy_pkg.b")
    mod_a = ModuleType("dummy_pkg.a")

    def digest_b(v, caller=None):
        return v

    def digest_a(v, caller=None):
        return v

    mod_b.digest_b = digest_b
    mod_a.digest_a = digest_a

    module_map = {
        "dummy_pkg": package,
        "dummy_pkg.a": mod_a,
        "dummy_pkg.b": mod_b,
    }

    monkeypatch.setattr(
        argument_loader.pkgutil,
        "iter_modules",
        lambda _path: [SimpleNamespace(name="b"), SimpleNamespace(name="a")],
    )
    monkeypatch.setattr(argument_loader, "import_module", lambda path: module_map[path])

    argument_loader._load_from_package.cache_clear()
    loaded = argument_loader.load_argument_digesters("dummy_pkg", "package")

    assert list(loaded.keys()) == ["a", "b"]
