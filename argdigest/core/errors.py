from __future__ import annotations
from typing import Any, TYPE_CHECKING

from .errors_base import ArgDigestCatalogException, ArgDigestCatalogWarning

if TYPE_CHECKING:
    from .context import Context

class DigestError(ArgDigestCatalogException):
    """Base class for all ArgDigest exceptions."""
    def __init__(self, message: str, context: Context | None = None, hint: str | None = None, code: str | None = None):
        self.raw_message = message
        self.context = context
        self.raw_hint = hint
        
        extra = {"message": message, "hint": hint or ""}
        if context:
            extra["argname"] = context.argname
            extra["caller"] = context.function_name
        else:
            extra["argname"] = "unknown"
            extra["caller"] = "unknown"

        super().__init__(message=message, code=code, extra=extra)

class DigestTypeError(DigestError, TypeError):
    """Unexpected or inconsistent data type."""
    catalog_key = "DigestTypeError"

class DigestValueError(DigestError, ValueError):
    """Invalid or out-of-domain value."""
    catalog_key = "DigestValueError"

class DigestInvariantError(DigestError):
    """Semantic rule violation (e.g. invalid parent-child link)."""
    catalog_key = "DigestInvariantError"

class DigestNotDigestedError(DigestError):
    """Missing digester or cyclic dependency."""
    catalog_key = "DigestNotDigestedError"

class DigestNotDigestedWarning(ArgDigestCatalogWarning, RuntimeWarning):
    """Warning for missing digesters when strictness is 'warn'."""
    catalog_key = "DigestNotDigestedWarning"

    def __init__(self, message: str, context: Context | None = None, hint: str | None = None, code: str | None = None):
        extra = {"message": message, "hint": hint or ""}
        if context:
            extra["argname"] = context.argname
            extra["caller"] = context.function_name
        else:
            extra["argname"] = "unknown"
            extra["caller"] = "unknown"
        
        super().__init__(message=message, code=code, extra=extra)
