from __future__ import annotations

from typing import Any

from ..core.errors import DigestTypeError, DigestValueError
from ..core.registry import register_pipeline


@register_pipeline(kind="feature", name="feature.base")
def feature_base(obj: Any, ctx):
    # example: require it to have `feature_id`
    if not hasattr(obj, "feature_id") and not (
        isinstance(obj, dict) and "feature_id" in obj
    ):
        raise DigestTypeError(
            context=ctx,
            detail=f"Argument '{ctx.argname}' in '{ctx.function_name}' must have 'feature_id'.",
        )
    return obj


@register_pipeline(kind="feature", name="feature.shape")
def feature_shape(obj: Any, ctx):
    # example: normalize shape_type to lowercase
    if isinstance(obj, dict) and "shape_type" in obj:
        obj["shape_type"] = str(obj["shape_type"]).lower()
        return obj

    if hasattr(obj, "shape_type"):
        val = getattr(obj, "shape_type")
        setattr(obj, "shape_type", str(val).lower())
        return obj

    raise DigestValueError(
        context=ctx,
        detail=f"Argument '{ctx.argname}' in '{ctx.function_name}' lacks 'shape_type'.",
    )
