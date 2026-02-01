from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Context:
    function_name: str
    argname: str
    value: Any
    all_args: dict[str, Any]
    audit_log: list[dict[str, Any]] = field(default_factory=list)

