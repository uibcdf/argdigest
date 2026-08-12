"""A decorated function must be called back the way it was declared.

Digestion works on a flat `name -> value` mapping, which is what makes a digester
reachable by argument name. Calling the function back with `**mapping` loses every
parameter that has no keyword form: `*args` cannot be addressed by name at all, and a
positional-only parameter refuses to be. These tests hold the call shape.
"""

import warnings

import pytest

from argdigest import arg_digest, argument_digest
from argdigest.core.utils import bind_arguments, build_call

# --- var-positional ---------------------------------------------------------------

def test_var_positional_survives_a_positional_call():
    @arg_digest(strictness="ignore")
    def combine(*items, tag=None):
        return items, tag

    assert combine("a", "b") == (("a", "b"), None)


def test_var_positional_reaches_the_function_as_separate_operands():
    """The tuple must arrive unpacked, not as one keyword carrying a tuple."""

    @arg_digest(strictness="ignore")
    def combine(first, *rest):
        return first, rest

    assert combine(1, 2, 3) == (1, (2, 3))


def test_var_positional_empty_is_still_empty():
    @arg_digest(strictness="ignore")
    def combine(*items):
        return items

    assert combine() == ()


def test_var_positional_with_keyword_only_and_var_keyword():
    @arg_digest(strictness="ignore")
    def combine(*items, tag=None, **extra):
        return items, tag, extra

    assert combine("a", "b", tag="x", other=1) == (("a", "b"), "x", {"other": 1})


def test_positional_or_keyword_before_a_filled_var_positional():
    """A non-empty `*rest` forces the earlier parameters to travel positionally."""

    @arg_digest(strictness="ignore")
    def combine(a, b=2, *rest):
        return a, b, rest

    assert combine(1, 5, 7, 9) == (1, 5, (7, 9))


def test_defaults_still_apply_around_a_var_positional():
    @arg_digest(strictness="ignore")
    def combine(*items, tag="default"):
        return items, tag

    assert combine("a") == (("a",), "default")


# --- positional-only --------------------------------------------------------------

def test_positional_only_parameter_survives():
    @arg_digest(strictness="ignore")
    def positioned(a, /, b=2):
        return a, b

    assert positioned(1, 3) == (1, 3)
    assert positioned(1) == (1, 2)
    assert positioned(1, b=4) == (1, 4)


def test_positional_only_together_with_var_positional():
    @arg_digest(strictness="ignore")
    def positioned(a, /, *rest, tag=None):
        return a, rest, tag

    assert positioned(1, 2, 3, tag="x") == (1, (2, 3), "x")


# --- the bypass path --------------------------------------------------------------

def test_skip_digestion_keyword_bypasses_without_losing_the_call_shape():
    @arg_digest(strictness="ignore")
    def combine(*items, skip_digestion=False):
        return items

    assert combine("a", "b", skip_digestion=True) == ("a", "b")


def test_skip_digestion_default_still_runs_digestion():
    @arg_digest(strictness="ignore")
    def combine(*items, skip_digestion=False):
        return items

    assert combine("a", "b") == ("a", "b")


# --- digestion still reaches the parameters ---------------------------------------

def test_var_positional_is_digested_as_one_tuple_under_its_own_name():
    """Documented behaviour: `*items` is bound as a single tuple and digested once.

    A digester named for the parameter therefore sees the whole collection, which is
    what lets it assert things about the group rather than about one operand.
    """

    seen = {}

    @argument_digest("items")
    def digest_items(items):
        seen["value"] = items
        return tuple(str(item).upper() for item in items)

    @arg_digest(digestion_style="decorator")
    def combine(*items):
        return items

    assert combine("a", "b") == ("A", "B")
    assert seen["value"] == ("a", "b")


def test_digestion_still_reaches_a_keyword_only_parameter():
    @argument_digest("tag")
    def digest_tag(tag):
        return None if tag is None else tag.upper()

    @arg_digest(digestion_style="decorator")
    def combine(*items, tag=None):
        return items, tag

    assert combine("a", tag="x") == (("a",), "X")


def test_pipelines_still_reach_a_positional_only_parameter():
    @arg_digest.map(name={"kind": "std", "rules": ["strip", "upper"]})
    def positioned(name, /):
        return name

    assert positioned("  ada  ") == "ADA"


def test_digestion_reaches_a_positional_only_parameter():
    @argument_digest("name")
    def digest_name(name):
        return name.upper()

    @arg_digest(digestion_style="decorator")
    def positioned(name, /, suffix=""):
        return name + suffix

    assert positioned("ada", suffix="!") == "ADA!"


# --- the contract layer keeps working on these signatures -------------------------

def test_unknown_keyword_is_still_refused_on_a_positional_only_signature():
    from argdigest import UnknownArgumentError

    @arg_digest(strictness="ignore")
    def positioned(name, /, count=1):
        return name, count

    with pytest.raises(UnknownArgumentError):
        positioned("ada", coumt=2)


def test_var_positional_name_is_not_reported_as_an_unknown_argument():
    @arg_digest(strictness="ignore")
    def combine(*items, tag=None):
        return items, tag

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert combine("a", "b", tag="x") == (("a", "b"), "x")


# --- the reconstruction helper itself ---------------------------------------------

def test_build_call_splits_a_signature_into_positional_and_keyword():
    import inspect

    def sample(a, /, b, *rest, tag=None, **extra):
        ...

    signature = inspect.signature(sample)
    bound = bind_arguments(sample, 1, 2, 3, 4, tag="x", other=9)
    args, kwargs = build_call(signature, bound)

    assert args == [1, 2, 3, 4]
    assert kwargs == {"tag": "x", "other": 9}


def test_build_call_keeps_named_parameters_as_keywords_when_nothing_forces_them():
    import inspect

    def sample(a, b=2):
        ...

    signature = inspect.signature(sample)
    bound = bind_arguments(sample, 1)
    args, kwargs = build_call(signature, bound)

    assert args == []
    assert kwargs == {"a": 1, "b": 2}
