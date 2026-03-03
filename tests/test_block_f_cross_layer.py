from __future__ import annotations

import smonitor
import pytest

from argdigest import DigestTypeError, DigestValueError, arg_digest
from argdigest.contrib import pyunitwizard_support as puw_support


def test_cross_layer_missing_puw_reemits_contract_error_with_context(monkeypatch):
    monkeypatch.setattr(puw_support, "HAS_PUW", False)

    @arg_digest.map(val={"kind": "q", "rules": [puw_support.is_quantity()]})
    def f(val):
        return val

    with pytest.raises(DigestTypeError) as excinfo:
        f(1.0)

    exc = excinfo.value
    assert exc.context is not None
    assert exc.context.function_name == "f"
    assert exc.context.argname == "val"
    assert exc.code == "ARG-ERR-TYPE-001"
    assert "install_optional:argdigest[pyunitwizard]" in exc.hint
    assert "DepDigest" in exc.hint


def test_cross_layer_convert_failure_reemits_value_error_with_context(monkeypatch):
    class FakePuw:
        @staticmethod
        def convert(_value, to_unit=None, to_form=None):
            raise RuntimeError(f"cannot convert to {to_unit}")

    monkeypatch.setattr(puw_support, "HAS_PUW", True)
    monkeypatch.setattr(puw_support, "puw", FakePuw)

    @arg_digest.map(dist={"kind": "q", "rules": [puw_support.convert(to_unit="nm")]})
    def g(dist):
        return dist

    with pytest.raises(DigestValueError) as excinfo:
        g("bad_quantity")

    exc = excinfo.value
    assert exc.context is not None
    assert exc.context.function_name == "g"
    assert exc.context.argname == "dist"
    assert exc.code == "ARG-ERR-VAL-001"


def test_cross_layer_diagnostics_coherent_between_user_and_dev_profiles(monkeypatch):
    monkeypatch.setattr(puw_support, "HAS_PUW", False)

    @arg_digest.map(val={"kind": "q", "rules": [puw_support.is_quantity()]})
    def h(val):
        return val

    try:
        smonitor.configure(profile="user")
        with pytest.raises(DigestTypeError) as excinfo_user:
            h(1.0)
        msg_user = str(excinfo_user.value)

        smonitor.configure(profile="dev")
        with pytest.raises(DigestTypeError) as excinfo_dev:
            h(1.0)
        msg_dev = str(excinfo_dev.value)
    finally:
        smonitor.configure(profile="user")

    assert msg_user != msg_dev
    assert "Check the expected type" in msg_user
    assert "Validate type logic" in msg_dev
