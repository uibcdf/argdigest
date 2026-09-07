from __future__ import annotations

from typing import TYPE_CHECKING

from .._private.smonitor.catalog import CATALOG
from .errors_base import ArgDigestCatalogException, ArgDigestCatalogWarning

if TYPE_CHECKING:
    from .context import Context


class DigestError(ArgDigestCatalogException):
    """Base class for all ArgDigest exceptions."""

    def __init__(
        self,
        message: str,
        context: Context | None = None,
        hint: str | None = None,
        code: str | None = None,
    ):
        self.context = context
        self.raw_hint = hint or ""
        resolved_code = code or CATALOG["exceptions"][self.catalog_key]["code"]
        # `code`, `message`, `raw_message` and `extra` belong to the catalog base
        # classes, which assign them last from what they are given below. Setting
        # them here writes into variables about to be overwritten. `hint` is not
        # theirs yet and stays until uibcdf/smonitor#5 lands it as a property.
        self.hint = self.raw_hint

        extra = {"message": message, "hint": self.hint, "code": resolved_code}
        if context:
            extra["argname"] = context.argname
            extra["caller"] = context.function_name
        else:
            extra["argname"] = "unknown"
            extra["caller"] = "unknown"

        super().__init__(message=message, code=resolved_code, extra=extra)


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

    def __init__(
        self,
        message: str,
        context: Context | None = None,
        hint: str | None = None,
        code: str | None = None,
    ):
        resolved_code = code or CATALOG["warnings"][self.catalog_key]["code"]
        # See `DigestError`: `code` is the base's to assign.
        self.hint = hint or ""
        extra = {"message": message, "hint": self.hint, "code": resolved_code}
        if context:
            extra["argname"] = context.argname
            extra["caller"] = context.function_name
        else:
            extra["argname"] = "unknown"
            extra["caller"] = "unknown"

        super().__init__(message=message, code=resolved_code, extra=extra)


class FunctionContractError(DigestError):
    """Base class for breaches of a function's argument contract (axis 1)."""

    catalog_key = "UnknownArgumentError"


class UnknownArgumentError(FunctionContractError):
    """An argument the function does not accept."""

    catalog_key = "UnknownArgumentError"


class MissingArgumentError(FunctionContractError):
    """A call that satisfies no required argument group."""

    catalog_key = "MissingArgumentError"


class ArgumentConsistencyError(FunctionContractError):
    """Mutually exclusive or co-required arguments used inconsistently."""

    catalog_key = "ArgumentConsistencyError"


class FunctionContractWarning(ArgDigestCatalogWarning, RuntimeWarning):
    """A contract breach reported instead of raised, under the 'warn' policy."""

    catalog_key = "FunctionContractWarning"

    def __init__(
        self,
        message: str,
        context: Context | None = None,
        hint: str | None = None,
        code: str | None = None,
    ):
        resolved_code = code or CATALOG["warnings"][self.catalog_key]["code"]
        # See `DigestError`: `code` is the base's to assign.
        self.hint = hint or ""
        extra = {"message": message, "hint": self.hint, "code": resolved_code}
        if context:
            extra["argname"] = context.argname
            extra["caller"] = context.function_name
        else:
            extra["argname"] = "unknown"
            extra["caller"] = "unknown"

        super().__init__(message=message, code=resolved_code, extra=extra)


class StandardizerContractError(DigestError):
    """A standardizer that did not honour `(caller, kwargs) -> mapping`.

    Forgetting the `return` is the common case, and without this the failure surfaces
    much later as `AttributeError: 'NoneType' object has no attribute 'items'`, which
    names neither the standardizer nor the library that configured it.
    """

    catalog_key = "StandardizerContractError"
