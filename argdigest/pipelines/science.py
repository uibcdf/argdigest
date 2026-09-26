from typing import Any, Optional

from ..core.registry import register_pipeline


def _numpy():
    try:
        import numpy
    except ImportError as error:
        raise ImportError(
            "numpy is required for scientific pipelines. Install argdigest[science]."
        ) from error
    return numpy


@register_pipeline(kind="sci", name="to_quantity_array")
def to_quantity_array(
    value: Any, ctx: Any = None, unit: Optional[str] = None, dtype: Any = "float64"
) -> Any:
    """
    Converts a value to a standardized numpy array, optionally extracting values from a quantity.
    Requires pyunitwizard to be available.
    """
    np = _numpy()
    try:
        from pyunitwizard import get_value
    except ImportError:
        # Fallback if pyunitwizard is not available in the environment
        if hasattr(value, "unit"):
            raise ImportError(
                "pyunitwizard is required to process quantities in argdigest."
            )
        val = value
    else:
        if unit is not None:
            val = get_value(value, to_unit=unit)
        else:
            val = get_value(value)

    target_dtype = np.dtype(dtype)
    if not isinstance(val, np.ndarray):
        val = np.asarray(val, dtype=target_dtype)
    elif val.dtype != target_dtype:
        val = val.astype(target_dtype)

    return val


@register_pipeline(kind="sci", name="to_float64_array")
def to_float64_array(value: Any, ctx: Any = None) -> Any:
    """Shortcut for to_quantity_array with float64."""
    return to_quantity_array(value, ctx, dtype="float64")


@register_pipeline(kind="sci", name="to_int64_array")
def to_int64_array(value: Any, ctx: Any = None) -> Any:
    """Shortcut for to_quantity_array with int64."""
    return to_quantity_array(value, ctx, dtype="int64")
