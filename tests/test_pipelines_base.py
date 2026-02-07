import pytest
from argdigest import arg_digest, DigestTypeError

def test_feature_base_pipeline():
    @arg_digest.map(feat={"kind": "feature", "rules": ["feature.base"]})
    def f(feat):
        return feat

    # Valid: has feature_id
    assert f({"feature_id": "f1"}) == {"feature_id": "f1"}

    # Invalid
    with pytest.raises(DigestTypeError, match="must have 'feature_id'"):
        f({"id": "f1"})

def test_feature_shape_pipeline():
    @arg_digest.map(feat={"kind": "feature", "rules": ["feature.shape"]})
    def f(feat):
        return feat

    # Valid
    res = f({"shape_type": "CONCAVITY"})
    assert res["shape_type"] == "concavity"