from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class Context:
    function_name: str
    argname: str
    value: Any
    all_args: dict[str, Any]

