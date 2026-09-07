import os
from typing import Any

from ..core.errors import DigestTypeError, DigestValueError
from ..core.registry import register_pipeline


@register_pipeline(kind="std", name="is_positive")
def is_positive(value: Any, ctx: Any = None) -> Any:
    """Validates that value is > 0."""
    if not (value > 0):
        raise DigestValueError(
            context=ctx, detail=f"Value must be positive, got {value}."
        )
    return value


@register_pipeline(kind="std", name="is_non_negative")
def is_non_negative(value: Any, ctx: Any = None) -> Any:
    """Validates that value is >= 0."""
    if not (value >= 0):
        raise DigestValueError(
            context=ctx, detail=f"Value must be non-negative, got {value}."
        )
    return value


@register_pipeline(kind="std", name="is_file")
def is_file(value: Any, ctx: Any = None) -> Any:
    """Validates that value is an existing file path."""
    if not os.path.isfile(value):
        raise DigestValueError(context=ctx, detail=f"File not found: {value}.")
    return value


@register_pipeline(kind="std", name="is_dir")
def is_dir(value: Any, ctx: Any = None) -> Any:
    """Validates that value is an existing directory."""
    if not os.path.isdir(value):
        raise DigestValueError(context=ctx, detail=f"Directory not found: {value}.")
    return value


# --- Type Validators ---


@register_pipeline(kind="std", name="is_int")
def is_int(value: Any, ctx: Any = None) -> int:
    """Strictly checks for int type."""
    if not isinstance(value, int):
        raise DigestTypeError(
            context=ctx, detail=f"Expected int, got {type(value).__name__}."
        )
    return value


@register_pipeline(kind="std", name="is_str")
def is_str(value: Any, ctx: Any = None) -> str:
    """Strictly checks for str type."""
    if not isinstance(value, str):
        raise DigestTypeError(
            context=ctx, detail=f"Expected str, got {type(value).__name__}."
        )
    return value
