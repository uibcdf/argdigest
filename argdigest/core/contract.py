from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

@dataclass(frozen=True, slots=True)
class ValidatedPayload:
    \"\"\"A lightweight 'Passport' for pre-validated scientific data.
    
    This object travels between functions to bypass redundant digestion 
    and unit normalization steps.
    \"\"\"
    value: Any
    unit: str
    dtype: str
    ndim: Optional[int] = None
    is_canonical: bool = True
    context: Optional[dict[str, Any]] = None

    def __repr__(self) -> str:
        return f"ValidatedPayload(unit={self.unit}, dtype={self.dtype}, ndim={self.ndim})"
