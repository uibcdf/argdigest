"""Execution selection must be independent of configuration transport."""

import importlib
from dataclasses import replace

import pytest

from argdigest import (
    DigestConfig,
    DigestNotDigestedError,
    DigestValueError,
    UnknownArgumentError,
    arg_digest,
    argument_digest,
)

MAP = {"value": {"kind": "std", "rules": ["strip", "upper"]}}


@pytest.mark.parametrize("selection", [True, False])
@pytest.mark.parametrize("transport", ["inline", "config", "map"])
def test_explicit_selection_is_independent_of_config_transport(selection, transport):
    if transport == "inline":
        decorate = arg_digest(map=MAP, strictness="error", argument_digestion=selection)
    elif transport == "config":
        decorate = arg_digest(
            map=MAP,
            config=DigestConfig(strictness="error", argument_digestion=selection),
        )
    else:
        decorate = arg_digest.map(
            config=DigestConfig(strictness="error"), argument_digestion=selection, **MAP
        )
    target = decorate(lambda value: value)
    assert target.digestion_plan.argument_digestion is selection
    assert target.digestion_plan.enable_argument_digestion is selection
    if selection:
        with pytest.raises(DigestNotDigestedError):
            target(" word ")
    else:
        assert target(" word ") == "WORD"


def test_unspecified_selection_preserves_historical_inference():
    implicit = arg_digest(map=MAP)(lambda value: value)
    configured = arg_digest(map=MAP, config=DigestConfig(strictness="error"))(
        lambda value: value
    )
    assert implicit.digestion_plan.argument_digestion is None
    assert configured.digestion_plan.argument_digestion is None
    assert implicit(" word ") == "WORD"
    with pytest.raises(DigestNotDigestedError):
        configured(" word ")


def test_pipeline_only_does_not_import_or_execute_argument_digesters():
    @argument_digest("value")
    def reject(value):
        pytest.fail("unselected digester executed")

    target = arg_digest(
        argument_digestion=False,
        digestion_source="absent_argument_source",
        map=MAP,
        config=DigestConfig(strictness="error"),
    )(lambda value: value)
    assert target(" word ") == "WORD"
    assert target.digestion_plan.digesters == {}


def test_argument_mode_runs_digesters_before_pipelines():
    @argument_digest("value")
    def digest(value):
        return str(value) + " digested"

    target = arg_digest(
        argument_digestion=True,
        digestion_style="decorator",
        strictness="error",
        map=MAP,
    )(lambda value: value)
    assert target("word") == "WORD DIGESTED"


def test_pipeline_only_still_binds_and_rejects_unknown_keywords():
    target = arg_digest(argument_digestion=False, map=MAP)(lambda value: value)
    with pytest.raises(UnknownArgumentError):
        target("word", typo="extra")
    with pytest.raises(TypeError):
        target("one", "two")


def test_pipeline_only_keeps_declared_contracts_and_aliases():
    from argdigest import ArgumentConsistencyError, MissingArgumentError
    from tests.mock_axis_one import api

    cfg = DigestConfig(
        function_source="tests.mock_axis_one._private.digestion.function",
        domain_source="tests.mock_axis_one._private.digestion.domain",
        normalization_source="tests.mock_axis_one._private.digestion.normalization",
        argument_digestion=False,
        strictness="error",
    )
    get = arg_digest(config=cfg)(api.get.__wrapped__)
    assert get("s", coords=True) == ["coordinates"]
    with pytest.raises(UnknownArgumentError):
        get("s", invalid_attribute=True)
    with pytest.raises(ArgumentConsistencyError):
        get("s", coords=True, coordinates=False)
    measure = arg_digest(config=cfg)(api.measure.__wrapped__)
    with pytest.raises(MissingArgumentError):
        measure("s")


def test_pipeline_only_keeps_standardizer_and_signature_shapes():
    def standardizer(caller, bound):
        return {**bound, "name": bound["name"].strip()}

    @arg_digest(
        argument_digestion=False,
        standardizer=standardizer,
        map={"name": {"kind": "std", "rules": ["upper"]}},
    )
    def target(name, /, *items, tag=None):
        return name, items, tag

    assert target(" name ", 1, 2, tag="x") == ("NAME", (1, 2), "x")


def test_pipeline_only_keeps_requested_type_checks():
    pytest.importorskip("beartype")
    from beartype.roar import BeartypeCallHintParamViolation

    @arg_digest(argument_digestion=False, type_check=True)
    def target(value: int):
        return value

    assert target(3) == 3
    with pytest.raises(BeartypeCallHintParamViolation):
        target("invalid")


def test_pipeline_only_classmethods_keep_receivers_in_both_orders():
    class Example:
        @classmethod
        @arg_digest(argument_digestion=False, map=MAP)
        def inner(cls, value):
            return cls, value

        @arg_digest(argument_digestion=False, map=MAP)
        @classmethod
        def outer(cls, value):
            return cls, value

    assert Example.inner(" word ") == (Example, "WORD")
    assert Example.outer(" word ") == (Example, "WORD")


def test_inline_selection_overrides_config_including_explicit_none():
    cfg = DigestConfig(argument_digestion=True, strictness="error")
    target = arg_digest(argument_digestion=False, config=cfg, map=MAP)(
        lambda value: value
    )
    assert target("word") == "WORD"
    inferred = arg_digest(
        argument_digestion=None, config=replace(cfg, argument_digestion=False), map=MAP
    )(lambda value: value)
    assert inferred.digestion_plan.argument_digestion is None
    with pytest.raises(DigestNotDigestedError):
        inferred("word")


@pytest.mark.parametrize("value", [0, 1, "false", "auto", []])
def test_selection_requires_literal_booleans_or_none(value):
    with pytest.raises(DigestValueError):
        arg_digest(argument_digestion=value)(lambda value: value)


@pytest.mark.parametrize("format", ["py", "yaml", "json"])
def test_selection_loads_from_files(tmp_path, format):
    from argdigest.config import load_from_file

    path = tmp_path / ("config." + format)
    path.write_text(
        {
            "py": "ARGUMENT_DIGESTION = False\nSTRICTNESS = 'error'",
            "yaml": "argument_digestion: false\nstrictness: error",
            "json": '{"argument_digestion": false, "strictness": "error"}',
        }[format]
    )
    cfg = load_from_file(path)
    target = arg_digest(config=cfg, map=MAP)(lambda value: value)
    assert cfg.argument_digestion is False
    assert target(" word ") == "WORD"


def test_selection_loads_from_module(tmp_path, monkeypatch):
    module = tmp_path / "selection_config.py"
    module.write_text("ARGUMENT_DIGESTION = False\nSTRICTNESS = 'error'")
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    target = arg_digest(config="selection_config", map=MAP)(lambda value: value)
    assert target(" word ") == "WORD"
