"""
Helpers to integrate ArgDigest with pydantic (v2-style).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type

from .._private.smonitor.catalog import CODES
from ..core.diagnostics import diagnostic_detail

if TYPE_CHECKING:
    from pydantic import BaseModel  # type: ignore


def model_from_dict(model_cls: Type["BaseModel"], data: Any) -> "BaseModel":
    if isinstance(data, model_cls):
        return data
    if isinstance(data, dict):
        return model_cls.model_validate(data)
    raise TypeError(
        diagnostic_detail(lambda: f"Cannot build {model_cls} from {type(data)}")
        or CODES["ARG-ERR-MODEL-001"]["metadata_message"]
    )


def pydantic_pipeline(model_cls: Type["BaseModel"]) -> callable:
    """
    Creates an ArgDigest pipeline function from a Pydantic model.
    The returned function takes (value, ctx) and returns a validated model instance.
    """

    def pipeline_fn(value: Any, ctx: Any) -> "BaseModel":
        # If it's already an instance, return it (Pydantic models are usually immutable-ish)
        if isinstance(value, model_cls):
            return value
        # Otherwise, let Pydantic coerce/validate it
        try:
            return model_cls.model_validate(value)
        except Exception as e:
            arg_info = f"argument '{ctx.argname}'" if ctx else "unknown argument"
            raise ValueError(
                diagnostic_detail(
                    lambda error=e: (
                        f"Pydantic validation failed for {arg_info}: {error}"
                    )
                )
                or CODES["ARG-ERR-MODEL-001"]["metadata_message"]
            ) from e

    return pipeline_fn
