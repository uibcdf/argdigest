import pytest
import numpy as np
from argdigest import arg_digest, DigestValueError, DigestTypeError
from argdigest.pipelines import data as data_pipelines

def test_numpy_coercion():
    @arg_arg_digest.map(arr={"kind": "data", "rules": ["to_numpy"]})
    def f(arr):
        return arr

    res = f([1, 2, 3])
    assert isinstance(res, np.ndarray)
    assert np.array_equal(res, np.array([1, 2, 3]))

def test_numpy_ndim_validation():
    @arg_arg_digest.map(matrix={"kind": "data", "rules": [data_pipelines.has_ndim(2)]})
    def f(matrix):
        return matrix

    # Valid 2D matrix
    f(np.zeros((3, 3)))
    
    # Invalid 1D array
    with pytest.raises(DigestValueError, match="Expected 2 dimensions"):
        f([1, 2, 3])

def test_numpy_shape_validation():
    @arg_arg_digest.map(vec={"kind": "data", "rules": [data_pipelines.is_shape((3,))]})
    def f(vec):
        return vec

    f(np.array([1, 2, 3]))
    
    with pytest.raises(DigestValueError, match="Dimension 0 mismatch"):
        f(np.array([1, 2]))

def test_numpy_dtype_validation():
    @arg_arg_digest.map(arr={"kind": "data", "rules": [data_pipelines.is_dtype('float64')]})
    def f(arr):
        return arr

    f(np.array([1.0, 2.0], dtype='float64'))
    
    with pytest.raises(DigestTypeError, match="Expected dtype float64"):
        f(np.array([1, 2], dtype='int32'))

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

@pytest.mark.skipif(not HAS_PANDAS, reason="pandas not installed")
def test_pandas_coercion():
    @arg_arg_digest.map(df={"kind": "data", "rules": ["to_dataframe"]})
    def f(df):
        return df

    res = f([{"a": 1}, {"a": 2}])
    assert isinstance(res, pd.DataFrame)
    assert list(res.columns) == ["a"]

@pytest.mark.skipif(not HAS_PANDAS, reason="pandas not installed")
def test_pandas_columns_validation():
    @arg_arg_digest.map(df={"kind": "data", "rules": ["to_dataframe", data_pipelines.has_columns(["id", "val"])]})
    def f(df):
        return df

    # Valid
    f({"id": [1], "val": [10]})
    
    # Missing columns
    with pytest.raises(DigestValueError, match="Missing columns"):
        f({"id": [1]})

@pytest.mark.skipif(not HAS_PANDAS, reason="pandas not installed")
def test_data_min_rows():
    # Test with numpy
    @arg_arg_digest.map(arr={"kind": "data", "rules": ["to_numpy", data_pipelines.min_rows(3)]})
    def f(arr):
        return arr

    f([1, 2, 3])
    with pytest.raises(DigestValueError, match="Expected at least 3 rows"):
        f([1, 2])

    # Test with pandas
    @arg_arg_digest.map(df={"kind": "data", "rules": ["to_dataframe", data_pipelines.min_rows(3)]})
    def g(df):
        return df

    g([{"a": 1}, {"a": 2}, {"a": 3}])
    with pytest.raises(DigestValueError, match="Expected at least 3 rows"):
        g([{"a": 1}])
