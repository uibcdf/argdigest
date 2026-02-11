import pytest

from argdigest import arg_digest
from argdigest.core.context import Context
from argdigest.core.errors import DigestNotDigestedWarning, DigestTypeError
from argdigest.pipelines import data as data_pipelines
from argdigest.contrib import pyunitwizard_support as puw_support


def test_missing_digester_warning_has_readable_message():
    @arg_digest(digestion_style="decorator", strictness="warn")
    def f(a):
        return a

    with pytest.warns(DigestNotDigestedWarning) as record:
        f("value")

    message = str(record[0].message)
    assert message.strip() != ""
    assert "digester" in message.lower()


def test_data_pipeline_missing_numpy_raises_catalog_error(monkeypatch):
    ctx = Context(function_name="f", argname="arr", value=[1, 2, 3], all_args={})
    monkeypatch.setattr(data_pipelines, "HAS_NUMPY", False)

    with pytest.raises(DigestTypeError) as excinfo:
        data_pipelines.to_numpy([1, 2, 3], ctx)

    message = str(excinfo.value)
    assert "numpy" in message.lower()
    assert message.strip() != ""


def test_contrib_pipeline_missing_pywizard_raises_catalog_error(monkeypatch):
    ctx = Context(function_name="f", argname="x", value="1 nm", all_args={})
    monkeypatch.setattr(puw_support, "HAS_PUW", False)

    pipeline = puw_support.check()
    with pytest.raises(DigestTypeError) as excinfo:
        pipeline("1 nm", ctx)

    message = str(excinfo.value)
    assert "pyunitwizard" in message.lower()
    assert message.strip() != ""
