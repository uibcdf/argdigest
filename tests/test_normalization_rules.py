"""Declared normalization: argument-name aliases as data.

Renaming has always been possible through the `standardizer` hook, one callable per
library that in practice grows a chain of `if caller == ...` branches. These tests cover
the declarative form: tables discovered like digesters and contracts, composed by
ArgDigest, and readable from outside.

The rules are static on purpose. Generating targets from a template such as
`{element}_{name}` is shorter to write and admits names that do not exist — on the
reference consumer it would have produced six attributes nobody defines.
"""

from __future__ import annotations

import pytest

from argdigest import (
    AliasTable,
    ArgumentConsistencyError,
    UnknownArgumentError,
    describe_normalization,
)
from argdigest.core.normalization import (
    NormalizationRegistry,
    apply_normalization,
)
from tests.mock_axis_one import api

# --- declaration ----------------------------------------------------------------------

def test_a_table_needs_at_least_one_alias():
    with pytest.raises(ValueError):
        AliasTable(aliases={})


def test_an_alias_to_itself_is_refused():
    # It can only be a mistake, and silently doing nothing would hide it.
    with pytest.raises(ValueError, match="maps to itself"):
        AliasTable(aliases={"group_index": "group_index"})


# --- resolution -----------------------------------------------------------------------

def test_a_global_table_applies_to_every_caller():
    registry = NormalizationRegistry([AliasTable(aliases={"residue_index": "group_index"})])

    for caller in ("pkg.a.f", "other.b.g"):
        assert apply_normalization(registry, caller, {"residue_index": 1}) == {"group_index": 1}


def test_a_caller_scoped_table_applies_only_there():
    registry = NormalizationRegistry([
        AliasTable(applies_to="pkg.basic.compare.compare",
                   aliases={"attributes_type": "attribute_type"}),
    ])

    assert apply_normalization(registry, "pkg.basic.compare.compare",
                               {"attributes_type": 1}) == {"attribute_type": 1}
    assert apply_normalization(registry, "pkg.basic.get.get",
                               {"attributes_type": 1}) == {"attributes_type": 1}


def test_a_pattern_covers_a_family():
    registry = NormalizationRegistry([
        AliasTable(applies_to="pkg.form.*", aliases={"idx": "index"}),
    ])

    assert apply_normalization(registry, "pkg.form.pdb.read", {"idx": 3}) == {"index": 3}
    assert apply_normalization(registry, "pkg.basic.get", {"idx": 3}) == {"idx": 3}


def test_the_more_specific_table_wins_for_the_same_name():
    registry = NormalizationRegistry([
        AliasTable(aliases={"name": "global_name"}),
        AliasTable(applies_to="pkg.get", aliases={"name": "specific_name"}),
    ])

    assert apply_normalization(registry, "pkg.get", {"name": 1}) == {"specific_name": 1}
    assert apply_normalization(registry, "pkg.other", {"name": 1}) == {"global_name": 1}


def test_a_context_guard_selects_between_tables():
    registry = NormalizationRegistry([
        AliasTable(applies_to="pkg.get", when={"element": "atom"},
                   aliases={"name": "atom_name"}),
        AliasTable(applies_to="pkg.get", when={"element": "group"},
                   aliases={"name": "group_name"}),
    ])

    assert apply_normalization(registry, "pkg.get", {"element": "atom", "name": "CA"}) == {
        "element": "atom", "atom_name": "CA"}
    assert apply_normalization(registry, "pkg.get", {"element": "group", "name": "ALA"}) == {
        "element": "group", "group_name": "ALA"}


def test_an_unmatched_guard_leaves_the_name_alone():
    registry = NormalizationRegistry([
        AliasTable(applies_to="pkg.get", when={"element": "atom"},
                   aliases={"name": "atom_name"}),
    ])

    assert apply_normalization(registry, "pkg.get", {"element": "chain", "name": "A"}) == {
        "element": "chain", "name": "A"}


def test_renaming_is_one_pass_never_a_chain():
    # If a -> b and b -> c, `a` becomes `b` and stops. Chaining would make the result
    # depend on declaration order, which nobody could reason about.
    registry = NormalizationRegistry([AliasTable(aliases={"a": "b", "b": "c"})])

    assert apply_normalization(registry, "pkg.f", {"a": 1}) == {"b": 1}


def test_argument_order_is_preserved():
    registry = NormalizationRegistry([AliasTable(aliases={"middle": "renamed"})])

    result = apply_normalization(registry, "pkg.f", {"first": 1, "middle": 2, "last": 3})
    assert list(result) == ["first", "renamed", "last"]


def test_an_empty_registry_returns_the_arguments_untouched():
    bound = {"a": 1}
    assert apply_normalization(NormalizationRegistry(), "pkg.f", bound) is bound


# --- collision contract --------------------------------------------------------------

def _assert_alias_collision(registry, bound, conflicting_names):
    with pytest.raises(ArgumentConsistencyError) as exc_info:
        apply_normalization(registry, "pkg.f", bound)

    assert exc_info.value.code == "ARG-ERR-CONTRACT-003"
    assert exc_info.value.context.function_name == "pkg.f"
    message = str(exc_info.value)
    assert "pkg.f" in message
    assert "coordinates" in message
    assert all(name in message for name in conflicting_names)


@pytest.mark.parametrize(
    "bound",
    [
        {"coords": True, "coordinates": False},
        {"coordinates": False, "coords": True},
        {"coords": True, "coordinates": True},
    ],
)
def test_an_alias_and_its_canonical_name_are_rejected_in_both_orders(bound):
    registry = NormalizationRegistry([AliasTable(aliases={"coords": "coordinates"})])

    _assert_alias_collision(registry, bound, {"coords", "coordinates"})


def test_two_supplied_aliases_with_one_target_are_rejected():
    registry = NormalizationRegistry([
        AliasTable(aliases={"coords": "coordinates"}),
        AliasTable(applies_to="pkg.f", aliases={"positions": "coordinates"}),
    ])

    _assert_alias_collision(
        registry,
        {"coords": True, "positions": False},
        {"coords", "positions"},
    )


def test_a_decorated_call_rejects_alias_and_canonical_before_its_body():
    with pytest.raises(ArgumentConsistencyError) as exc_info:
        api.get("s", coords=True, coordinates=False)

    assert exc_info.value.code == "ARG-ERR-CONTRACT-003"
    assert exc_info.value.context.function_name == "tests.mock_axis_one.api.get"
    message = str(exc_info.value)
    assert "tests.mock_axis_one.api.get" in message
    assert "coordinates" in message
    assert "coords" in message


# --- introspection --------------------------------------------------------------------

def test_the_declared_aliases_can_be_read_back():
    registry = NormalizationRegistry([
        AliasTable(aliases={"residue_index": "group_index"}, description="anatomy"),
        AliasTable(applies_to="pkg.get", aliases={"attr": "attribute"}),
    ])

    described = describe_normalization(registry, caller="pkg.get")

    # This is the point of declaring rules as data: what a function also accepts can be
    # listed in its documentation instead of living inside a branch of a standardizer.
    assert {entry["applies_to"] for entry in described} == {"*", "pkg.get"}
    assert any(entry["description"] == "anatomy" for entry in described)


# --- end to end, through the real discovery path ---------------------------------------

@pytest.mark.parametrize("keyword,expected", [
    ("coords", "coordinates"),
    ("n_atomz", "n_atoms"),
    ("attr", "n_bonds"),
])
def test_declared_aliases_reach_the_call(keyword, expected):
    assert api.get("s", **{keyword: True}) == [expected]


@pytest.mark.parametrize("element,expected", [("atom", "n_atoms"), ("bond", "n_bonds")])
def test_a_context_guarded_alias_reaches_the_call(element, expected):
    assert api.get("s", element=element, name=True) == [expected]


def test_an_alias_survives_the_function_contract():
    # The guarantee that makes the two mechanisms composable: normalization runs first,
    # so by the time the contract judges a keyword it is already canonical. Declaring a
    # contract must never break a library's aliases.
    assert api.get("s", coords=True) == ["coordinates"]


def test_a_genuine_typo_is_still_refused():
    # It survives normalization unchanged and then fails the contract, which is the whole
    # point of running them in this order.
    with pytest.raises(UnknownArgumentError, match="n_atomzz"):
        api.get("s", n_atomzz=True)


# --- defaults are not a second name --------------------------------------------------

def test_a_default_is_not_counted_as_a_supplied_name():
    """A canonical name resting on its default is not a competing alias.

    `bind_arguments` applies defaults, so by the time normalization sees the call it
    cannot tell `attribute_type=None` (filled in from the signature) from a value the
    caller wrote. Counting both made every alias whose target has a default a collision:
    passing only `coords` was rejected because `coordinates` was "also present".
    """
    bound = {"coords": True, "coordinates": None}
    registry = NormalizationRegistry([
        AliasTable(applies_to="pkg.f", aliases={"coords": "coordinates"}),
    ])

    # Only `coords` came from the caller.
    result = apply_normalization(registry, "pkg.f", bound, supplied={"coords"})
    assert result["coordinates"] is True
    assert "coords" not in result


def test_both_names_supplied_is_still_a_collision():
    """The rule itself is unchanged: writing both really is ambiguous."""
    bound = {"coords": True, "coordinates": False}
    registry = NormalizationRegistry([
        AliasTable(applies_to="pkg.f", aliases={"coords": "coordinates"}),
    ])

    with pytest.raises(ArgumentConsistencyError):
        apply_normalization(registry, "pkg.f", bound, supplied={"coords", "coordinates"})


def test_a_decorated_call_accepts_an_alias_whose_target_has_a_default():
    """End to end, through the decorator that binds and applies the defaults."""
    assert api.get("s", coords=True) == ["coordinates"]
