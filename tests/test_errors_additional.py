from __future__ import annotations

from argdigest.core.errors import DigestNotDigestedWarning, DigestTypeError


def test_digest_type_error_without_context():
    err = DigestTypeError("bad type")
    assert "bad type" in str(err)


def test_digest_not_digested_warning_without_context():
    warn = DigestNotDigestedWarning("missing digester")
    assert "missing digester" in str(warn)
