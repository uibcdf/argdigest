"""Declared contract identity must remain independent of inherited display identity."""

import itertools
import json
import sys
import types
from dataclasses import replace

import pytest

from argdigest import (
    AliasTable,
    ArgumentConsistencyError,
    DigestConfig,
    Domain,
    FunctionContract,
    UnknownArgumentError,
    arg_digest,
    argument_digest,
)
from argdigest.core.caller import resolve_contract_owner, validate_contract_owner
from argdigest.core.config import load_from_file

_modules = itertools.count()


@pytest.fixture
def library(monkeypatch):
    """Define genuine module-scope methods, exercising the non-<locals> branch."""

    def make(owner="definition"):
        name = f"owner37_base_{next(_modules)}"
        module = types.ModuleType(name)
        exec(
            """
class Methods:
    def accept(self, value=None, left=None, right=None, **kwargs):
        return value, kwargs

    def closed(self, value):
        return value

    def build(cls, value):
        return cls.__name__, value

    def static(value):
        return value
""",
            module.__dict__,
        )
        monkeypatch.setitem(sys.modules, name, module)
        key = f"{name}.accept" if owner in (None, "definition") else owner
        declarations = types.ModuleType(f"{name}_declarations")
        declarations.TABLES = [AliasTable({"short": "value"}, applies_to=key)]
        declarations.CONTRACTS = [
            FunctionContract(
                caller=key,
                admits="options",
                mutually_exclusive=[("left", "right")],
            )
        ]
        declarations.DOMAINS = [Domain("options", members=("extra",))]
        monkeypatch.setitem(sys.modules, declarations.__name__, declarations)
        seen = []

        @argument_digest("value")
        def digest_value(value, caller=None, qualname=None, contract_owner=None):
            seen.append(("digest", caller, qualname, contract_owner))
            return None if value is None else int(value)

        for argument in ("left", "right", "short", "extra"):
            argument_digest(argument)(lambda value: value)

        def standardize(caller, bound):
            seen.append(("standardizer", caller, dict(bound)))
            return bound

        config = DigestConfig(
            contract_owner=owner,
            digestion_style="decorator",
            strictness="error",
            standardizer=standardize,
            function_source=declarations.__name__,
            domain_source=declarations.__name__,
            normalization_source=declarations.__name__,
        )
        Base = type(
            "Base",
            (),
            {
                "__module__": name,
                "accept": arg_digest(config=config)(module.Methods.accept),
            },
        )
        Child = type("Child", (Base,), {"__module__": f"{name}_external"})
        return types.SimpleNamespace(
            Base=Base, Child=Child, config=config, module=module, key=key, seen=seen
        )

    return make


@pytest.mark.parametrize("owner", ["definition", "logical.constructor.accept"])
def test_inherited_stages_share_declared_identity_and_keep_runtime_display(
    library, owner
):
    lib = library(owner)
    assert lib.Child().accept(short="7", extra="allowed") == (7, {"extra": "allowed"})
    assert lib.seen[0][0:2] == ("standardizer", lib.key)
    assert lib.seen[0][2]["value"] == "7"
    assert "short" not in lib.seen[0][2]
    assert lib.seen[1] == (
        "digest",
        lib.key,
        f"{lib.Child.__module__}.Child.accept",
        None,
    )
    plan = lib.Child.accept.digestion_plan
    assert plan.contract_owner == owner
    assert plan.contract_caller == lib.key
    with pytest.raises(ArgumentConsistencyError) as refusal:
        lib.Child().accept(value=7, left=1, right=2)
    assert f"{lib.Child.__module__}.Child.accept" in str(refusal.value)
    with pytest.raises(UnknownArgumentError):
        lib.Child().accept(value=7, misspelled=1)
    with pytest.raises(ValueError):
        lib.Child().accept(value="invalid integer")


def test_default_preserves_runtime_contract_and_mixin_dispatch(library):
    lib = library(None)
    assert lib.Base().accept(short="7") == (7, {})
    with pytest.raises(ArgumentConsistencyError):
        lib.Base().accept(value=7, left=1, right=2)
    lib.seen.clear()
    assert lib.Child().accept(value=2, left=1, right=2) == (2, {})
    assert lib.seen[0][1] == f"{lib.Child.__module__}.accept"
    assert lib.seen[1][1:3] == (
        f"{lib.Child.__module__}.accept",
        f"{lib.Child.__module__}.Child.accept",
    )
    assert lib.Child.accept.digestion_plan.contract_caller is None
    MixinAPI = type("MixinAPI", (lib.Base,), {"__module__": "consumer.assembled"})
    lib.seen.clear()
    assert MixinAPI().accept(value=3) == (3, {})
    assert lib.seen[1][1] == "consumer.assembled.accept"


def test_definition_follows_inherited_implementation_and_overrides(library):
    left, right = library(), library()
    Combined = type("Combined", (left.Base, right.Base), {"__module__": "consumer.api"})
    Deep = type("Deep", (Combined,), {"__module__": "consumer.deep"})
    assert Deep().accept(short="4") == (4, {})
    assert left.seen[-1][1:3] == (left.key, "consumer.deep.Deep.accept")
    Override = type(
        "Override",
        (Combined,),
        {"__module__": "consumer.override", "accept": right.Base.accept},
    )
    assert Override().accept(short="5") == (5, {})
    assert right.seen[-1][1:3] == (right.key, "consumer.override.Override.accept")


@pytest.mark.parametrize("owner", ["definition", "logical.api.method"])
@pytest.mark.parametrize("descriptor", ["class_outer", "class_inner", "static"])
def test_inherited_descriptor_contract_identity(library, owner, descriptor):
    lib = library(owner)
    fn = (
        lib.module.Methods.static
        if descriptor == "static"
        else lib.module.Methods.build
    )
    decorate = arg_digest(config=replace(lib.config, function_source=None))
    if descriptor == "class_outer":
        method = classmethod(decorate(fn))
    elif descriptor == "class_inner":
        method = decorate(classmethod(fn))
    else:
        method = staticmethod(decorate(fn))
    Parent = type("Parent", (), {"method": method, "__module__": "consumer.parent"})
    Child = type("Child", (Parent,), {"__module__": "consumer.child"})
    result = Child.method("6")
    assert result == (6 if descriptor == "static" else ("Child", 6))
    key = f"{lib.module.__name__}.{fn.__name__}" if owner == "definition" else owner
    display = (
        f"{lib.module.__name__}.Methods.static"
        if descriptor == "static"
        else "consumer.child.Child.build"
    )
    assert lib.seen[-1][1:3] == (key, display)


def test_closed_signature_cannot_override_policy_through_call_arguments(library):
    lib = library()
    method = arg_digest(config=lib.config)(lib.module.Methods.closed)
    Base = type("Base", (), {"closed": method, "__module__": lib.module.__name__})
    assert Base().closed("3") == 3
    with pytest.raises(UnknownArgumentError):
        Base().closed("3", contract_owner="other.api.closed")
    assert method.digestion_plan.contract_caller == f"{lib.module.__name__}.closed"


def test_existing_decorator_context_name_is_not_reserved(library):
    lib = library()
    method = arg_digest(config=lib.config, contract_owner="existing-context")(
        lib.module.Methods.closed
    )
    Base = type("Base", (), {"closed": method, "__module__": lib.module.__name__})
    assert Base().closed("3") == 3
    assert lib.seen[-1][1:] == (
        f"{lib.module.__name__}.closed",
        f"{lib.module.__name__}.Base.closed",
        "existing-context",
    )


@pytest.mark.parametrize("owner", ["definition", "logical.api.accept"])
def test_map_form_retains_contracts_when_value_digesters_are_disabled(library, owner):
    lib = library(owner)
    config = replace(lib.config, argument_digestion=False)
    wrapped = arg_digest.map(
        config=config,
        value={"kind": "owner37", "rules": [lambda value, ctx: int(value)]},
    )(lib.module.Methods.accept)
    Child = type("Child", (), {"accept": wrapped, "__module__": "consumer.child"})
    assert Child().accept(short="8") == (8, {})
    assert not any(row[0] == "digest" for row in lib.seen)
    with pytest.raises(ArgumentConsistencyError):
        Child().accept(value=8, left=1, right=2)


@pytest.mark.parametrize("transport", ["module", "py", "json", "yaml"])
@pytest.mark.parametrize("owner", ["definition", "logical.api.closed"])
def test_configuration_transports_select_the_same_contract(
    library, monkeypatch, tmp_path, transport, owner
):
    lib = library()
    data = {
        "contract_owner": owner,
        "digestion_style": "decorator",
        "strictness": "error",
    }
    if transport in ("module", "py"):
        text = "\n".join(f"{name.upper()} = {value!r}" for name, value in data.items())
        if transport == "module":
            module = types.ModuleType(f"{lib.module.__name__}_config")
            exec(text, module.__dict__)
            monkeypatch.setitem(sys.modules, module.__name__, module)
            config = module.__name__
        else:
            path = tmp_path / "config.py"
            path.write_text(text)
            config = load_from_file(path)
    else:
        path = tmp_path / f"config.{transport}"
        # JSON is also valid YAML and exercises the ordinary YAML loader.
        path.write_text(json.dumps(data))
        config = load_from_file(path)
    wrapped = arg_digest(config=config)(lib.module.Methods.closed)
    Child = type("Child", (), {"closed": wrapped, "__module__": "consumer.child"})
    assert Child().closed("9") == 9
    key = f"{lib.module.__name__}.closed" if owner == "definition" else owner
    assert lib.seen[-1][1:3] == (key, "consumer.child.Child.closed")


@pytest.mark.parametrize("owner", [True, 1, [], {}, object()])
def test_non_string_owner_is_refused(owner):
    with pytest.raises(TypeError, match="contract_owner"):
        DigestConfig(contract_owner=owner)


@pytest.mark.parametrize(
    "owner",
    [
        "",
        "runtime",
        "pkg.*",
        "pkg.fn ",
        " pkg.fn",
        "pkg..fn",
        "pkg:fn",
        "pkg.class",
        "pkg.fn()",
    ],
)
def test_invalid_key_is_refused_at_configuration_time(owner):
    with pytest.raises(ValueError, match="contract_owner"):
        DigestConfig(contract_owner=owner)


def test_reusable_owner_resolution_uses_existing_caller_convention():
    assert validate_contract_owner(None) is None
    assert (
        resolve_contract_owner(
            test_reusable_owner_resolution_uses_existing_caller_convention, None
        )
        is None
    )
    assert (
        resolve_contract_owner(
            test_reusable_owner_resolution_uses_existing_caller_convention, "definition"
        )
        == f"{__name__}.test_reusable_owner_resolution_uses_existing_caller_convention"
    )
    with pytest.raises(TypeError, match="named callable"):
        resolve_contract_owner(object(), "definition")
