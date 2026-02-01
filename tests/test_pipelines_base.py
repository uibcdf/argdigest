import pytest
from argdigest import digest, DigestTypeError, DigestValueError

def test_feature_base_pipeline():
    @digest.map(feat={"kind": "feature", "rules": ["feature.base"]})
    def f(feat):
        return feat

    # Valid: has feature_id
    assert f({"feature_id": "f1"}) == {"feature_id": "f1"}
    
    # Invalid
    with pytest.raises(DigestTypeError, match="must have 'feature_id'"):
        f({"other": 1})

def test_feature_shape_pipeline():
    @digest.map(feat={"kind": "feature", "rules": ["feature.shape"]})
    def f(feat):
        return feat

    # Valid
    res = f({"shape_type": "CONCAVITY"})
    assert res["shape_type"] == "concavity"
    
    # Invalid
    with pytest.raises(DigestValueError, match="lacks 'shape_type'"):
        f({"other": 1})
