import pytest

from argdigest import arg_digest
from argdigest.core.argument_registry import ArgumentRegistry


def test_method_digester_receives_runtime_qualname_without_changing_caller(monkeypatch):
    observed = []

    def digest_method_label_probe(value, caller=None, qualname=None):
        observed.append((caller, qualname))
        return value

    monkeypatch.setattr(
        ArgumentRegistry,
        "_digesters",
        {"method_label_probe": digest_method_label_probe},
    )

    class Base:
        @arg_digest(digestion_style="decorator", strictness="error")
        def method(self, method_label_probe):
            return method_label_probe

        @classmethod
        @arg_digest(digestion_style="decorator", strictness="error")
        def build(cls, method_label_probe):
            return method_label_probe

    class Child(Base):
        pass

    assert Child().method("instance") == "instance"
    assert Child.build("class") == "class"
    Runtime = type("Runtime", (Base,), {"__module__": "suite.runtime"})
    assert Runtime().method("mixin") == "mixin"
    assert observed == [
        (f"{__name__}.method", f"{__name__}.Child.method"),
        (f"{__name__}.build", f"{__name__}.Child.build"),
        (f"{__name__}.method", "suite.runtime.Runtime.method"),
    ]


def test_qualname_is_optional_and_can_name_refusal(monkeypatch):
    def digest_method_label_probe(value, qualname=None):
        raise ValueError(f"{qualname} cannot take {value!r}")

    monkeypatch.setattr(
        ArgumentRegistry,
        "_digesters",
        {"method_label_probe": digest_method_label_probe},
    )

    class Resolver:
        @arg_digest(digestion_style="decorator", strictness="error")
        def resolve(self, method_label_probe):
            return method_label_probe

    with pytest.raises(ValueError, match=r"Resolver\.resolve cannot take 'bad'"):
        Resolver().resolve("bad")
