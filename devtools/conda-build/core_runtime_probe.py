"""Exercise the installed minimal core without scientific dependencies."""

from __future__ import annotations

import importlib.util
import sys


class OwnershipMethods:
    """Module-scope methods exercise runtime dispatch across module boundaries."""

    def accept(self, release_value):
        return release_value

    def static_inner(release_value):
        return release_value

    def static_outer(release_value):
        return release_value


def main() -> None:
    assert importlib.util.find_spec("numpy") is None, "Core solve installed NumPy"
    from argdigest import (
        DigestConfig,
        DigestError,
        arg_digest,
        argument_digest,
        register_diagnostics,
    )
    from argdigest.pipelines.coercers import to_bool
    from argdigest.pipelines.science import to_quantity_array

    assert "numpy" not in sys.modules
    assert to_bool("yes") is True
    try:
        to_quantity_array([1, 2])
    except ImportError as error:
        assert "argdigest[science]" in str(error)
    else:
        raise AssertionError("Missing science extra was silently accepted")

    seen = []

    @argument_digest("release_value")
    def digest_value(release_value, caller=None, qualname=None):
        seen.append((caller, qualname))
        return int(release_value)

    @argument_digest("skip_digestion")
    def digest_skip(skip_digestion):
        if type(skip_digestion) is not bool:
            raise TypeError("skip_digestion must be bool")
        return skip_digestion

    class Base:
        @classmethod
        @arg_digest(digestion_style="decorator", strictness="error")
        def inner(cls, release_value, skip_digestion=False):
            return cls, release_value

        @arg_digest(digestion_style="decorator", strictness="error")
        @classmethod
        def outer(cls, release_value, skip_digestion=False):
            return cls, release_value

    class Child(Base):
        pass

    assert Child.inner("5") == (Child, 5)
    assert Child.outer("6") == (Child, 6)
    assert seen[0][0].endswith(".inner")
    assert seen[0][1].endswith(".Child.inner")
    assert seen[1][1].endswith(".Child.outer")
    assert Child.inner("5", skip_digestion=True) == (Child, "5")
    for invalid in ("yes", "False", 1):
        try:
            Child.inner("5", skip_digestion=invalid)
        except TypeError as error:
            assert "skip_digestion must be bool" in str(error)
        else:
            raise AssertionError("A truthy nonboolean bypassed digestion")

    for owner in (None, "definition", "release_contract.base.accept"):
        config = DigestConfig(
            digestion_style="decorator", strictness="error", contract_owner=owner
        )
        owned_base = type(
            "OwnershipBase",
            (),
            {
                "__module__": __name__,
                "accept": arg_digest(config=config)(OwnershipMethods.accept),
                "static_inner": staticmethod(
                    arg_digest(config=config)(OwnershipMethods.static_inner)
                ),
                "static_outer": arg_digest(config=config)(
                    staticmethod(OwnershipMethods.static_outer)
                ),
            },
        )
        owned_child = type(
            "OwnershipChild", (owned_base,), {"__module__": "release_consumer.child"}
        )
        instance = owned_child()
        assert instance.accept("7") == 7
        expected_key = (
            "release_consumer.child.accept"
            if owner is None
            else f"{__name__}.accept"
            if owner == "definition"
            else owner
        )
        assert seen[-1] == (
            expected_key,
            "release_consumer.child.OwnershipChild.accept",
        )
        plan = owned_child.accept.digestion_plan
        assert plan.contract_owner == owner
        assert plan.contract_caller == (None if owner is None else expected_key)
        for receiver in (owned_child, instance):
            for name in ("static_inner", "static_outer"):
                assert getattr(receiver, name)("8") == 8
                static_key = (
                    owner if owner not in (None, "definition") else f"{__name__}.{name}"
                )
                assert seen[-1] == (
                    static_key,
                    f"{__name__}.OwnershipMethods.{name}",
                )
        try:
            instance.accept("invalid")
        except ValueError:
            pass
        else:
            raise AssertionError("Explicit ownership bypassed value validation")
    assert "numpy" not in sys.modules

    @arg_digest.map(
        config=DigestConfig(argument_digestion=False, strictness="error"),
        name={"kind": "std", "rules": ["strip", "upper"]},
    )
    def normalize(name):
        return name

    assert normalize(" name ") == "NAME"
    assert normalize.digestion_plan.argument_digestion is False
    assert normalize.digestion_plan.enable_argument_digestion is False
    try:
        arg_digest(capture_policy="metadata_only")(lambda value: value)
    except DigestError as error:
        assert error.code == "ARG-ERR-CAPTURE-001"
    else:
        raise AssertionError(
            "A lower-bound provider silently accepted restrictive capture"
        )
    try:
        register_diagnostics()
    except RuntimeError as error:
        assert "bootstrap_policy=False" in str(error)
    else:
        raise AssertionError(
            "A lower-bound provider silently accepted registration-only diagnostics"
        )
    assert "numpy" not in sys.modules
    print(
        "PASS: NumPy-free core, science remedy, classmethods, qualname, bypass, "
        "contract ownership, staticmethods, explicit pipelines, "
        "restrictive and registration-only refusals "
        "on the lower-bound provider"
    )


if __name__ == "__main__":
    main()
