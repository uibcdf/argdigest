import sys
from pathlib import Path


def _add_examples_to_path():
    root = Path(__file__).resolve().parents[1]
    examples_dir = root / "examples"
    sys.path.insert(0, str(examples_dir))


def test_packlib_package_style():
    _add_examples_to_path()
    from packlib import get, get_auto

    item, selection, syntax = get("x", selection=None)
    assert selection == "all"
    assert item == "x"
    assert syntax == "PackLib"

    item, selection, syntax = get_auto("x", selection=None)
    assert selection == "all"
    assert item == "x"
    assert syntax == "PackLib"


def test_reglib_registry_style_dual_mode():
    _add_examples_to_path()
    from reglib import analyze

    a, b = analyze("2", "3")
    assert a == 4
    assert b == 5
