from argdigest import digest

def test_legacy_package_style_with_injection():
    """
    Tests that ArgDigest can load digesters from a package (MolSysMT style)
    and inject arguments like 'syntax' into them.
    """
    @digest(config="tests.mock_molsysmt._argdigest")
    def select(selection, syntax="MolSysMT"):
        return selection

    # 1. Default syntax
    res = select("all")
    assert res == "Selection: all, Syntax: MolSysMT"

    # 2. Custom syntax
    res2 = select("1-10", syntax="Amber")
    assert res2 == "Selection: 1-10, Syntax: Amber"

def test_legacy_injection_missing_optional():
    """
    If the digester asks for 'syntax' but the function doesn't have it,
    ArgDigest currently passes None if it's not in bound args?
    Actually, ArgDigest injects None for params in digester signature that aren't in bound args.
    Let's verify this behavior is what we want (tolerance).
    """
    @digest(config="tests.mock_molsysmt._argdigest")
    def simple_select(selection):
        return selection

    # The digester expects 'syntax'. It's not in simple_select.
    # ArgDigest should inject None.
    res = simple_select("atoms")
    # Our mock digester returns "Syntax: None"
    assert res == "Selection: atoms, Syntax: None"
