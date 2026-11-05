"""The VAR_KEYWORD parameter name is also a legal literal keyword."""

import sys
import types

import pytest

from argdigest import (
    AliasTable,
    DigestConfig,
    Domain,
    FunctionContract,
    UnknownArgumentError,
    arg_digest,
)


@pytest.mark.parametrize("name", ["kwargs", "options"])
@pytest.mark.parametrize("bypass", [False, True])
@pytest.mark.parametrize("kind", ["opaque", "mapping", "none", "empty"])
def test_literal_var_keyword_preserves_native_value_identity(name, bypass, kind):
    namespace = {"__name__": __name__}
    exec(
        f"def delegate(file_name, skip_digestion=False, **{name}):\n"
        f"    return file_name, {name}\n",
        namespace,
    )
    original = namespace["delegate"]
    wrapped = arg_digest(config=DigestConfig(argument_digestion=False))(original)
    payload = {
        "opaque": object(),
        "mapping": {"file_name": "changed", "selection": object()},
        "none": None,
        "empty": {},
    }[kind]
    kwargs = {name: payload, "skip_digestion": bypass}
    expected = original("original", **kwargs)
    actual = wrapped("original", **kwargs)
    assert actual == expected
    assert actual[0] == "original"
    assert actual[1][name] is payload


def test_literal_var_keyword_with_positional_only_and_variadic_arguments():
    @arg_digest(config=DigestConfig(argument_digestion=False))
    def delegate(file_name, /, *items, **options):
        return file_name, items, options

    payload = {"file_name": "changed"}
    assert delegate("original", 1, 2, options=payload) == (
        "original",
        (1, 2),
        {"options": payload},
    )


@pytest.mark.parametrize("admitted", [True, False])
def test_literal_keyword_alias_is_admitted_or_refused_without_expansion(
    monkeypatch, admitted
):
    declarations = types.ModuleType(f"literal_keyword_contracts_{admitted}")
    caller = f"{__name__}.delegate"
    declarations.TABLES = [AliasTable({"short": "options"}, applies_to=caller)]
    declarations.CONTRACTS = [FunctionContract(caller=caller, admits="payload")]
    declarations.DOMAINS = [Domain("payload", members=("options",) if admitted else ())]
    monkeypatch.setitem(sys.modules, declarations.__name__, declarations)
    seen = []

    @arg_digest(
        config=DigestConfig(
            argument_digestion=False,
            normalization_source=declarations.__name__,
            function_source=declarations.__name__,
            domain_source=declarations.__name__,
        )
    )
    def delegate(file_name, **options):
        seen.append(file_name)
        return file_name, options

    payload = {"file_name": "changed"}
    if admitted:
        result = delegate("original", short=payload)
        assert result == ("original", {"options": payload})
        assert result[1]["options"] is payload
    else:
        with pytest.raises(UnknownArgumentError):
            delegate("original", options=payload)
        assert seen == []
