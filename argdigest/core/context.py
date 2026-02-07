from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Context:
    function_name: str
    argname: str
    value: Any
    all_args: dict[str, Any] = field(default_factory=dict)
    audit_log: list[dict[str, Any]] | None = None
    _profiling: bool = False