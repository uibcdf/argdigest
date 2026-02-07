from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .context import Context

class DigestError(Exception):
    """Base class for all ArgDigest exceptions."""
    def __init__(self, message: str, context: Context | None = None, hint: str | None = None):
        self.message = message
        self.context = context
        self.hint = hint
        super().__init__(self._build_full_message())

    def _build_full_message(self) -> str:
        if self.context is None:
            return self.message
        
        ctx_msg = f"Argument '{self.context.argname}' from '{self.context.function_name}' failed."
        full = f"{ctx_msg} {self.message}"
        if self.hint:
            full += f" Hint: {self.hint}"
        return full

class DigestTypeError(DigestError, TypeError):
    """Unexpected or inconsistent data type."""
    pass

class DigestValueError(DigestError, ValueError):
    """Invalid or out-of-domain value."""
    pass

class DigestInvariantError(DigestError):
    """Semantic rule violation (e.g. invalid parent-child link)."""
    pass

class DigestNotDigestedError(DigestError):
    """Missing digester or cyclic dependency."""
    pass

class DigestNotDigestedWarning(RuntimeWarning):
    """Warning for missing digesters when strictness is 'warn'."""
    pass