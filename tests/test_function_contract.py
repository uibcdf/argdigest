"""Axis 1: the function argument contract.

ArgDigest's original axis answers "is this argument's value valid?". These tests cover
the other one: "may this function receive this argument at all, and does it have what
it needs?".

The guiding rule is that ArgDigest must never be more permissive than the language it
wraps. Plain Python raises TypeError for an unexpected keyword; a decorated function
must not start accepting it.
"""

from __future__ import annotations

import warnings

import pytest

from argdigest import (
    ArgumentConsistencyError,
    Domain,
    FunctionContract,
    FunctionContractError,
    FunctionContractWarning,
    MissingArgumentError,
    UnknownArgumentError,
    arg_digest,
    describe_contract,
)
from argdigest.core.function_contract import (
    ContractRegistry,
    check_contract,
    default_contract,
)


ATTRIBUTES = {"n_atoms", "n_bonds", "coordinates"}


@pytest.fixture()
def domains():
    return {
        "attribute": Domain(
            name="attribute",
            contains=lambda keyword: keyword in ATTRIBUTES,
            members=lambda: ATTRIBUTES,
            description="canonical attribute names",
        )
    }


# --- Domain -------------------------------------------------------------------------

def test_a_domain_needs_a_way_to_decide_membership():
    with pytest.raises(ValueError):
        Domain(name="empty")


def test_a_domain_can_be_defined_by_members_alone():
    domain = Domain(name="colour", members=("red", "blue"))
    assert "red" in domain
    assert "green" not in domain
    assert set(domain.known_members()) == {"red", "blue"}


def test_a_domain_defined_only_by_a_predicate_is_not_enumerable():
    domain = Domain(name="even", contains=lambda k: k.isdigit() and int(k) % 2 == 0)
    assert "4" in domain
    assert domain.known_members() == ()


# --- contract declaration -------------------------------------------------------------

def test_a_contract_targets_a_caller_or_a_pattern_but_not_both():
    with pytest.raises(ValueError):
        FunctionContract(caller="a.b", caller_pattern="a.*")
    with pytest.raises(ValueError):
        FunctionContract()


def test_the_default_contract_follows_the_signature_of_a_closed_function():
    contract = default_contract("pkg.fn", has_var_keyword=False)
    assert contract.admits == "signature"


def test_the_default_contract_admits_anything_when_the_function_opened_the_door():
    contract = default_contract("pkg.fn", has_var_keyword=True)
    assert contract.admits_anything()


# --- resolution order -----------------------------------------------------------------

def test_an_exact_caller_wins_over_a_pattern():
    exact = FunctionContract(caller="pkg.mod.fn", admits="any")
    pattern = FunctionContract(caller_pattern="pkg.*", admits="signature")
    registry = ContractRegistry([pattern, exact])

    assert registry.resolve("pkg.mod.fn") is exact
    assert registry.resolve("pkg.other.fn") is pattern


def test_the_longest_matching_pattern_wins():
    broad = FunctionContract(caller_pattern="pkg.*", admits="signature")
    narrow = FunctionContract(caller_pattern="pkg.form.*.to_file_h5msm", admits="any")
    registry = ContractRegistry([broad, narrow])

    assert registry.resolve("pkg.form.pdb.to_file_h5msm") is narrow
    assert registry.resolve("pkg.form.pdb.other") is broad


def test_an_unmatched_caller_resolves_to_nothing():
    registry = ContractRegistry([FunctionContract(caller_pattern="other.*")])
    assert registry.resolve("pkg.fn") is None


# --- checking -------------------------------------------------------------------------

def test_an_unknown_keyword_is_a_violation(domains):
    contract = FunctionContract(caller="pkg.fn")
    violations = check_contract(contract, "pkg.fn", {"selection"}, ["bogus"], domains)

    assert [v.kind for v in violations] == ["unknown_argument"]
    assert violations[0].keyword == "bogus"


def test_the_violation_suggests_a_near_miss(domains):
    contract = FunctionContract(caller="pkg.fn")
    violations = check_contract(
        contract, "pkg.fn", {"structure_indices"}, ["structure_indeces"], domains)

    assert "structure_indices" in violations[0].hint


def test_a_keyword_in_an_admitted_domain_is_accepted(domains):
    contract = FunctionContract(caller="pkg.fn", admits="attribute")
    assert check_contract(contract, "pkg.fn", {"element"}, ["n_atoms"], domains) == []


def test_admitting_anything_accepts_anything(domains):
    contract = FunctionContract(caller="pkg.fn", admits="any")
    assert check_contract(contract, "pkg.fn", {"element"}, ["whatever"], domains) == []


def test_a_contract_naming_an_unregistered_domain_is_reported(domains):
    contract = FunctionContract(caller="pkg.fn", admits="nonexistent")
    kinds = [v.kind for v in check_contract(contract, "pkg.fn", set(), [], domains)]
    assert "unknown_domain" in kinds


def test_requires_any_of_is_satisfied_by_one_member(domains):
    contract = FunctionContract(caller="pkg.fn", admits="attribute",
                                requires_any_of="attribute")
    assert check_contract(contract, "pkg.fn", {"element"}, ["n_atoms"], domains,
                          present={"n_atoms"}) == []


def test_requires_any_of_is_violated_when_nothing_is_asked(domains):
    contract = FunctionContract(caller="pkg.fn", admits="attribute",
                                requires_any_of="attribute")
    violations = check_contract(contract, "pkg.fn", {"element"}, [], domains,
                                present={"element"})
    assert [v.kind for v in violations] == ["missing_argument"]


def test_mutually_exclusive_arguments(domains):
    contract = FunctionContract(caller="pkg.fn", mutually_exclusive=[("a", "b")])
    violations = check_contract(contract, "pkg.fn", {"a", "b"}, [], domains,
                                present={"a", "b"})
    assert [v.kind for v in violations] == ["mutually_exclusive"]


def test_co_required_arguments(domains):
    contract = FunctionContract(caller="pkg.fn", co_required=[("a", "b")])
    violations = check_contract(contract, "pkg.fn", {"a", "b"}, [], domains,
                                present={"a"})
    assert [v.kind for v in violations] == ["co_required"]
    assert check_contract(contract, "pkg.fn", {"a", "b"}, [], domains,
                          present={"a", "b"}) == []


# --- introspection --------------------------------------------------------------------

def test_a_contract_describes_itself_as_data(domains):
    contract = FunctionContract(caller="pkg.get", admits="attribute",
                                requires_any_of="attribute",
                                description="asks for attributes")
    described = describe_contract(contract, domains)

    # This is what makes the real domain of a **kwargs function readable, which
    # inspect.signature cannot show.
    assert described["caller"] == "pkg.get"
    assert described["admitted_domains"][0]["name"] == "attribute"
    assert described["admitted_domains"][0]["registered"] is True
    assert set(described["admitted_domains"][0]["members"]) == ATTRIBUTES


# --- end to end, through the real discovery path -------------------------------------
#
# These go through `tests/mock_axis_one`, a consumer package that declares both axes in
# its own `_argdigest.py`. That is the path a real library uses; reaching into the
# decorator's closure to inject a registry would test a route nobody travels.

from tests.mock_axis_one import api  # noqa: E402


def test_a_closed_function_rejects_an_unknown_keyword():
    assert api.extract('s', structure_indices=[0]) == [0]
    with pytest.raises(UnknownArgumentError, match='structure_indeces'):
        api.extract('s', structure_indeces=[0])


def test_the_rejection_suggests_the_intended_name():
    with pytest.raises(UnknownArgumentError, match='structure_indices'):
        api.extract('s', structure_indeces=[0])


def test_an_open_function_is_held_to_its_declared_domain():
    assert api.get('s', n_atoms=True) == ['n_atoms']
    with pytest.raises(UnknownArgumentError, match='n_atomss'):
        api.get('s', n_atomss=True)


def test_a_declared_requirement_is_enforced():
    assert api.measure('s', n_bonds=True) == ['n_bonds']
    with pytest.raises(MissingArgumentError):
        api.measure('s')


def test_a_family_pattern_covers_a_function_with_no_exact_contract():
    assert api.to_file_pdb('s', path='out.pdb') == 'out.pdb'
    with pytest.raises(UnknownArgumentError, match='pathh'):
        api.to_file_pdb('s', pathh='out.pdb')


def test_mutually_exclusive_arguments_are_refused_at_the_call():
    assert api.pick('s', by_name='x') == 'x'
    with pytest.raises(ArgumentConsistencyError):
        api.pick('s', by_name='x', by_index=1)


def test_an_open_function_without_a_declared_domain_still_admits_anything():
    # The documented default. A library is never broken by a domain it has not written.
    assert api.wide_open('s', anything=1) == ['anything']


def test_skip_digestion_bypasses_the_contract_and_python_catches_it_instead():
    # The escape hatch escapes both axes, as it must to stay an escape hatch. What it
    # cannot do is make the call *less* safe than an undecorated function: with the
    # contract skipped, the keyword reaches Python and Python refuses it.
    assert api.extract('s', structure_indices=[0], skip_digestion=True) == [0]
    with pytest.raises(TypeError, match='structure_indeces'):
        api.extract('s', structure_indeces=[0], skip_digestion=True)


def test_argdigest_is_never_more_permissive_than_python():
    # The property the whole axis exists to restore.
    def plain(molsys, selection='all'):
        return selection

    with pytest.raises(TypeError):
        plain('s', bogus=1)

    with pytest.raises(UnknownArgumentError):
        api.extract('s', bogus=1)
