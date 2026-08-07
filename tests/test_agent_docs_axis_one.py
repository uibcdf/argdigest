"""
The generated agent instructions must describe both axes.

`ARG_DIGEST_AGENTS.md` is written by the CLI and tells an agent what to do when it edits
a library. Until it mentioned the function argument contract, an agent reading it in full
would conclude ArgDigest only validates values, and would never declare a contract for a
function taking `**kwargs` -- leaving it accepting anything.

This is also where `describe_contract` earns the design decision behind it: a contract is
data rather than an opaque callable precisely so the accepted domain of a `**kwargs`
function can be rendered, which `inspect.signature` cannot do.
"""

from __future__ import annotations

from argdigest import Domain, FunctionContract
from argdigest.core.agent_docs import _render_axis_one
from argdigest.core.function_contract import ContractRegistry


ATTRIBUTES = ("n_atoms", "n_bonds", "coordinates")


def _domains():
    return {
        "attribute": Domain(
            name="attribute",
            contains=lambda keyword: keyword in ATTRIBUTES,
            members=lambda: ATTRIBUTES,
            description="canonical attribute names",
        )
    }


def test_the_declared_domain_and_its_size_are_rendered():
    registry = ContractRegistry([
        FunctionContract(caller="pkg.basic.get.get", admits="attribute"),
    ])

    rendered = _render_axis_one(registry, _domains())

    assert "`attribute`" in rendered
    assert "3" in rendered
    assert "canonical attribute names" in rendered
    assert "`pkg.basic.get.get`" in rendered


def test_a_requirement_is_rendered():
    registry = ContractRegistry([
        FunctionContract(caller="pkg.basic.get.get", admits="attribute",
                         requires_any_of="attribute"),
    ])

    assert "attribute" in _render_axis_one(registry, _domains())


def test_a_pattern_contract_is_rendered_by_its_pattern():
    registry = ContractRegistry([
        FunctionContract(caller_pattern="pkg.form.*.to_file_h5msm", admits="signature"),
    ])

    assert "pkg.form.*.to_file_h5msm" in _render_axis_one(registry, {})


def test_a_library_declaring_nothing_is_told_what_that_means():
    rendered = _render_axis_one(ContractRegistry(), {})

    # Silence here would read as "nothing to do". It has to say that closed signatures
    # are still protected and that **kwargs functions are not.
    assert "closed signature" in rendered
    assert "admit anything" in rendered


def test_unloadable_declarations_are_reported_rather_than_hidden():
    assert "could not be loaded" in _render_axis_one(None, {})
