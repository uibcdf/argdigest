"""
Helpers to integrate ArgDigest with pydantic (v2-style).
"""

from __future__ import annotations
from typing import Any, Type
from pydantic import BaseModel  # type: ignore


def model_from_dict(model_cls: Type[BaseModel], data: Any) -> BaseModel:
    if isinstance(data, model_cls):
        return data
    if isinstance(data, dict):
        return model_cls.model_validate(data)
    raise TypeError(f"Cannot build {model_cls} from {type(data)}")
