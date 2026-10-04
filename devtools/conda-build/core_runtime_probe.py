"""Exercise the installed minimal core without scientific dependencies."""

from __future__ import annotations

import importlib.util
import sys


def main() -> None:
    assert importlib.util.find_spec("numpy") is None, "Core solve installed NumPy"
    from argdigest import arg_digest, argument_digest
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
    assert "numpy" not in sys.modules
    print("PASS: NumPy-free core, science remedy, classmethods, qualname and bypass")


if __name__ == "__main__":
    main()
