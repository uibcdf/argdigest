import pytest

from argdigest import DigestValueError, arg_digest


def test_feature_shape_pipeline_with_object_attribute():
    class FeatureObj:
        def __init__(self):
            self.shape_type = "CONVEX"

    @arg_digest.map(feat={"kind": "feature", "rules": ["feature.shape"]})
    def f(feat):
        return feat

    obj = FeatureObj()
    result = f(obj)
    assert result.shape_type == "convex"


def test_feature_shape_pipeline_missing_shape_raises():
    class FeatureObj:
        pass

    @arg_digest.map(feat={"kind": "feature", "rules": ["feature.shape"]})
    def f(feat):
        return feat

    with pytest.raises(DigestValueError, match="lacks 'shape_type'"):
        f(FeatureObj())
