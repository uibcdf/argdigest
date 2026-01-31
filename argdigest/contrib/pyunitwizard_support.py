"""
Integration with PyUnitWizard for physical quantity validation and standardization.
"""
from __future__ import annotations
from typing import Any, Dict, Optional, Callable
from contextlib import contextmanager

try:
    import pyunitwizard as puw
    HAS_PUW = True
except ImportError:
    HAS_PUW = False

from ..core.errors import DigestValueError, DigestTypeError

def _require_puw():
    if not HAS_PUW:
        raise ImportError("pyunitwizard is not installed. Install it to use these pipelines.")

@contextmanager
def context(**kwargs: Any):
    """
    Context manager that delegates to pyunitwizard.context if available.
    If PUW is not installed, it yields without doing anything (unless kwargs are passed, then warning/error?).
    Assuming if user passes puw_context, they expect PUW to work.
    """
    if not HAS_PUW:
        if kwargs:
            # If user requested context but PUW is missing, warn or ignore?
            # For robustness, let's ignore but maybe log a debug message if we had access to logger here.
            pass
        yield
        return

    # Map kwargs to puw.context parameters if names differ?
    # ArgDigest config might use 'form' instead of 'default_form'.
    # Let's map them for convenience.
    
    puw_kwargs = {}
    if 'form' in kwargs:
        puw_kwargs['default_form'] = kwargs.pop('form')
    if 'parser' in kwargs:
        puw_kwargs['default_parser'] = kwargs.pop('parser')
    
    # Pass rest (like standard_units) directly
    puw_kwargs.update(kwargs)
    
    with puw.context(**puw_kwargs):
        yield

# --- Factories for Pipelines ---

def check(
    dimensionality: Optional[Dict[str, int]] = None,
    value_type: Optional[Any] = None,
    shape: Optional[tuple] = None,
    unit: Optional[str] = None,
) -> Callable[[Any, Any], Any]:
    """
    Returns a pipeline function that uses puw.check() to validate the input.
    """
    _require_puw()

    def pipeline_check(value: Any, ctx: Any) -> Any:
        # puw.check returns True/False
        valid = puw.check(
            value,
            dimensionality=dimensionality,
            value_type=value_type,
            shape=shape,
            unit=unit
        )
        if not valid:
            raise DigestValueError(
                f"Physical validation failed for {ctx.argname}. "
                f"Expected dimensionality={dimensionality}, unit={unit}, type={value_type}",
                context=ctx
            )
        return value

    pipeline_check.__name__ = "puw.check"
    return pipeline_check


def standardize() -> Callable[[Any, Any], Any]:
    """
    Returns a pipeline function that calls puw.standardize().
    It respects the global pyunitwizard configuration (form/units).
    """
    _require_puw()

    def pipeline_standardize(value: Any, ctx: Any) -> Any:
        try:
            return puw.standardize(value)
        except Exception as e:
            raise DigestValueError(f"Standardization failed: {e}", context=ctx) from e

    pipeline_standardize.__name__ = "puw.standardize"
    return pipeline_standardize


def convert(to_unit: str, to_form: Optional[str] = None) -> Callable[[Any, Any], Any]:
    """
    Returns a pipeline function that converts the quantity to a specific unit/form.
    """
    _require_puw()

    def pipeline_convert(value: Any, ctx: Any) -> Any:
        try:
            return puw.convert(value, to_unit=to_unit, to_form=to_form)
        except Exception as e:
            raise DigestValueError(f"Conversion to {to_unit} failed: {e}", context=ctx) from e

    pipeline_convert.__name__ = f"puw.convert({to_unit})"
    return pipeline_convert


def is_quantity() -> Callable[[Any, Any], Any]:
    _require_puw()
    def pipeline_is_quantity(value: Any, ctx: Any) -> Any:
        if not puw.is_quantity(value):
             raise DigestTypeError(f"Expected a quantity, got {type(value)}", context=ctx)
        return value
    pipeline_is_quantity.__name__ = "puw.is_quantity"
    return pipeline_is_quantity