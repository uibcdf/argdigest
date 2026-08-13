"""
Integration with PyUnitWizard for physical quantity validation and standardization.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Callable
from contextlib import contextmanager

import numpy as np

try:
    import pyunitwizard as puw
    HAS_PUW = True
    puw = puw # Export for tests
except ImportError:
    HAS_PUW = False

from ..core.errors import DigestValueError, DigestTypeError
from ..core.registry import register_pipeline


def _require_puw(ctx: Any = None):
    if not HAS_PUW:
        raise DigestTypeError(
            "Optional dependency 'pyunitwizard' is not installed. Install it to use PyUnitWizard pipelines.",
            context=ctx,
            hint=(
                "install_optional:argdigest[pyunitwizard] "
                "(pip install argdigest[pyunitwizard]); "
                "if your host library uses DepDigest, enable its pyunitwizard capability."
            ),
        )

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
    def pipeline_check(value: Any, ctx: Any) -> Any:
        _require_puw(ctx)
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
    def pipeline_standardize(value: Any, ctx: Any) -> Any:
        _require_puw(ctx)
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
    def pipeline_convert(value: Any, ctx: Any) -> Any:
        _require_puw(ctx)
        try:
            return puw.convert(value, to_unit=to_unit, to_form=to_form)
        except Exception as e:
            raise DigestValueError(f"Conversion to {to_unit} failed: {e}", context=ctx) from e

    pipeline_convert.__name__ = f"puw.convert({to_unit})"
    return pipeline_convert


def is_quantity() -> Callable[[Any, Any], Any]:
    def pipeline_is_quantity(value: Any, ctx: Any) -> Any:
        _require_puw(ctx)
        if not puw.is_quantity(value):
             raise DigestTypeError(f"Expected a quantity, got {type(value)}", context=ctx)
        return value
    pipeline_is_quantity.__name__ = "puw.is_quantity"
    return pipeline_is_quantity


def _canonical_array_pipeline(
    unit_name: str,
    specialized_name: str,
    ndim: Optional[int] = None,
) -> Callable[[Any, Any], np.ndarray]:
    """Canonicalize a quantity to `unit_name` as a float64 array.

    It returns the array, not a container carrying it. An earlier version returned a
    `ValidatedPayload` so that a downstream call could recognise the value as already
    canonical -- which required every function body in between to know about the box,
    and a companion rule to take the value back out of it. The mechanism found no user
    and cost every reader of a decorated function an extra concept, so it is gone.
    """

    def pipeline_canonical(value: Any, ctx: Any) -> np.ndarray:
        _require_puw(ctx)
        try:
            # Handle nested attributes like fast_track.to_nanometers
            normalizer = puw
            for part in specialized_name.split("."):
                normalizer = getattr(normalizer, part)
            canonical = normalizer(value)
            raw = np.asarray(puw.get_value(canonical), dtype=np.float64)
        except Exception as e:
            raise DigestValueError(
                f"Canonical normalization to {unit_name} failed: {e}",
                context=ctx,
            ) from e

        if ndim is not None and raw.ndim != ndim:
            raise DigestValueError(
                (
                    f"Normalized value for {ctx.argname} has ndim={raw.ndim}; "
                    f"expected ndim={ndim}."
                ),
                context=ctx,
            )

        return raw

    pipeline_canonical.__name__ = f"sci:{unit_name}_float64"
    return pipeline_canonical


def nm_float64(ndim: Optional[int] = None) -> Callable[[Any, Any], np.ndarray]:
    return _canonical_array_pipeline("nm", "fast_track.to_nanometers", ndim=ndim)


def ps_float64(ndim: Optional[int] = None) -> Callable[[Any, Any], np.ndarray]:
    return _canonical_array_pipeline("ps", "fast_track.to_picoseconds", ndim=ndim)


def kelvin_float64(ndim: Optional[int] = None) -> Callable[[Any, Any], np.ndarray]:
    return _canonical_array_pipeline("kelvin", "fast_track.to_kelvin", ndim=ndim)


@register_pipeline(kind="sci", name="nm_float64")
def _pipeline_nm_float64(value: Any, ctx: Any) -> np.ndarray:
    return nm_float64()(value, ctx)


@register_pipeline(kind="sci", name="ps_float64")
def _pipeline_ps_float64(value: Any, ctx: Any) -> np.ndarray:
    return ps_float64()(value, ctx)


@register_pipeline(kind="sci", name="kelvin_float64")
def _pipeline_kelvin_float64(value: Any, ctx: Any) -> np.ndarray:
    return kelvin_float64()(value, ctx)
