from argdigest import arg_digest


def _molsysmt_get_standardizer(caller, kwargs):
    """Mimic MolSysMT get-name rewriting: name -> <element>_name."""
    caller_name = caller.rsplit(".", 1)[-1] if isinstance(caller, str) else getattr(caller, "__name__", "")
    if caller_name != "get":
        return kwargs
    if "name" not in kwargs:
        return kwargs
    if "element" not in kwargs:
        return kwargs

    out = dict(kwargs)
    element = out.get("element")
    out[f"{element}_name"] = out.pop("name")
    return out


def test_molsysmt_like_get_standardizer_with_package_digestion():
    @arg_digest(
        config="tests.mock_molsysmt._argdigest",
        strictness="ignore",
        standardizer=_molsysmt_get_standardizer,
    )
    def get(selection=None, syntax="MolSysMT", element="atom", **kwargs):
        return selection, kwargs

    selection, kwargs = get(selection="all", element="atom", name="CA")
    assert selection == "Selection: all, Syntax: MolSysMT"
    assert kwargs["atom_name"] == "CA"
    assert "name" not in kwargs

    selection, kwargs = get(selection="protein", element="group", name="backbone")
    assert selection == "Selection: protein, Syntax: MolSysMT"
    assert kwargs["group_name"] == "backbone"
    assert "name" not in kwargs


def test_molsysmt_like_get_standardizer_keeps_kwargs_when_not_applicable():
    @arg_digest(
        config="tests.mock_molsysmt._argdigest",
        strictness="ignore",
        standardizer=_molsysmt_get_standardizer,
    )
    def get(selection=None, syntax="MolSysMT", element="atom", **kwargs):
        return selection, kwargs

    selection, kwargs = get(selection="all", element="atom", label="CA")
    assert selection == "Selection: all, Syntax: MolSysMT"
    assert kwargs["label"] == "CA"
    assert "atom_name" not in kwargs
