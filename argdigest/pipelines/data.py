"""
Pipelines for data science structures (Numpy, Pandas, etc.).
"""
from __future__ import annotations
from typing import Any, Callable, Tuple, List
from ..core.registry import register_pipeline
from ..core.errors import DigestTypeError, DigestValueError

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def _require_numpy():
    if not HAS_NUMPY:
        raise ImportError("numpy is not installed. Install it to use these pipelines.")


def _require_pandas():
    if not HAS_PANDAS:
        raise ImportError("pandas is not installed. Install it to use these pipelines.")

# --- Coercers ---

@register_pipeline(kind="data", name="to_numpy")
def to_numpy(value: Any, ctx: Any = None) -> Any:
    """Coerces input to a numpy array."""
    _require_numpy()
    if isinstance(value, np.ndarray):
        return value
    try:
        return np.asarray(value)
    except Exception as e:
        raise DigestTypeError(f"Cannot convert to numpy array: {e}", context=ctx) from e


@register_pipeline(kind="data", name="to_dataframe")
def to_dataframe(value: Any, ctx: Any = None) -> Any:
    """Coerces input to a pandas DataFrame."""
    _require_pandas()
    if isinstance(value, pd.DataFrame):
        return value
    try:
        return pd.DataFrame(value)
    except Exception as e:
        raise DigestTypeError(f"Cannot convert to pandas DataFrame: {e}", context=ctx) from e

# --- Parameterized Factories ---

def has_ndim(n: int) -> Callable[[Any, Any], Any]:
    """Factory: Validates number of dimensions."""
    _require_numpy()
    def pipeline_ndim(value: Any, ctx: Any) -> Any:
        arr = value if isinstance(value, np.ndarray) else np.asarray(value)
        if arr.ndim != n:
            raise DigestValueError(f"Expected {n} dimensions, got {arr.ndim}", context=ctx)
        return value
    pipeline_ndim.__name__ = f"has_ndim({n})"
    return pipeline_ndim

def is_shape(shape: Tuple[int | None, ...]) -> Callable[[Any, Any], Any]:
    """
    Factory: Validates array shape. 
    Use None for any size in a dimension: (None, 3).
    """
    _require_numpy()
    def pipeline_shape(value: Any, ctx: Any) -> Any:
        arr = value if isinstance(value, np.ndarray) else np.asarray(value)
        if len(arr.shape) != len(shape):
             raise DigestValueError(f"Expected ndim={len(shape)}, got {len(arr.shape)}", context=ctx)
        
        for i, (actual, expected) in enumerate(zip(arr.shape, shape)):
            if expected is not None and actual != expected:
                raise DigestValueError(f"Dimension {i} mismatch: expected {expected}, got {actual}", context=ctx)
        return value
    pipeline_shape.__name__ = f"is_shape({shape})"
    return pipeline_shape

def is_dtype(dtype: Any) -> Callable[[Any, Any], Any]:
    """Factory: Validates numpy dtype."""
    _require_numpy()
    def pipeline_dtype(value: Any, ctx: Any) -> Any:
        arr = value if isinstance(value, np.ndarray) else np.asarray(value)
        target_dtype = np.dtype(dtype)
        if arr.dtype != target_dtype:
            raise DigestTypeError(f"Expected dtype {target_dtype}, got {arr.dtype}", context=ctx)
        return value
    pipeline_dtype.__name__ = f"is_dtype({dtype})"
    return pipeline_dtype

def has_columns(columns: List[str]) -> Callable[[Any, Any], Any]:
    """Factory: Validates that a DataFrame has specific columns."""
    _require_pandas()
    def pipeline_columns(value: Any, ctx: Any) -> Any:
        if not isinstance(value, pd.DataFrame):
            # Try to coerce if it's not a dataframe? 
            # Better to be strict here and rely on to_dataframe pipeline if needed.
            raise DigestTypeError(f"Expected DataFrame, got {type(value).__name__}", context=ctx)
        
        missing = [col for col in columns if col not in value.columns]
        if missing:
            raise DigestValueError(f"Missing columns in DataFrame: {missing}", context=ctx)
        return value
    pipeline_columns.__name__ = f"has_columns({columns})"
    return pipeline_columns

def min_rows(n: int) -> Callable[[Any, Any], Any]:
    """Factory: Validates minimum number of rows in a DataFrame or Array."""
    def pipeline_min_rows(value: Any, ctx: Any) -> Any:
        # Works for both numpy and pandas
        if hasattr(value, "__len__"):
            length = len(value)
        elif hasattr(value, "shape"):
            length = value.shape[0]
        else:
            raise DigestTypeError(f"Object of type {type(value).__name__} has no length", context=ctx)
            
        if length < n:
            raise DigestValueError(f"Expected at least {n} rows, got {length}", context=ctx)
        return value
    pipeline_min_rows.__name__ = f"min_rows({n})"
    return pipeline_min_rows