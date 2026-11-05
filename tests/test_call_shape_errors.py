"""Call-shape refusals retain the Python TypeError catch family."""

import copy
import pickle

import pytest

from argdigest import (
    DigestConfig,
    MissingArgumentError,
    UnknownArgumentError,
    arg_digest,
)
from argdigest.core.errors import (
    ArgumentConsistencyError,
    DigestError,
    FunctionContractError,
)


@pytest.mark.parametrize("bypass", [None, False, True])
@pytest.mark.parametrize("mapping", [False, True])
def test_closed_signature_unknown_keyword_is_typeerror_before_body(bypass, mapping):
    seen = []
    decorator = arg_digest.map if mapping else arg_digest

    @decorator(
        config=DigestConfig(argument_digestion=False, contract_owner="definition")
    )
    def read(file_name, skip_digestion=False):
        seen.append(file_name)

    kwargs = {"typo": True}
    if bypass is not None:
        kwargs["skip_digestion"] = bypass
    with pytest.raises(TypeError) as caught:
        read("file.json", **kwargs)
    assert seen == []
    if bypass is not True:
        assert isinstance(caught.value, UnknownArgumentError)
        assert isinstance(caught.value, FunctionContractError)
        assert caught.value.code == "ARG-ERR-CONTRACT-001"
        assert caught.value.extra["argname"] == "typo"


@pytest.mark.parametrize("error_type", [UnknownArgumentError, MissingArgumentError])
def test_typed_catalog_errors_keep_existing_catches_and_rebuild(error_type):
    error = error_type(detail="Invalid call shape")
    assert isinstance(error, (TypeError, DigestError))
    assert isinstance(error, TypeError) and isinstance(error, DigestError)
    for rebuilt in (
        type(error)(*error.args),
        copy.deepcopy(error),
        pickle.loads(pickle.dumps(error)),
    ):
        assert type(rebuilt) is error_type
        assert isinstance(rebuilt, TypeError)
        assert rebuilt.code == error.code
        assert rebuilt.args == error.args
    assert not isinstance(ArgumentConsistencyError(), TypeError)
