from __future__ import annotations

from typing import TYPE_CHECKING

from .._private.smonitor.catalog import CATALOG
from .errors_base import ArgDigestCatalogException, ArgDigestCatalogWarning

if TYPE_CHECKING:
    from .context import Context


def _context_extra(context: Context | None, **fields: object) -> dict[str, object]:
    """The structured payload every catalog template here interpolates.

    `argname` and `caller` are what the templates name, and they are the two
    facts a `Context` carries. A raise site with no context still emits both, as
    `"unknown"`, so a template never renders a hole.
    """
    extra: dict[str, object] = {
        "argname": context.argname if context else "unknown",
        "caller": context.function_name if context else "unknown",
    }
    extra.update({key: value for key, value in fields.items() if value is not None})
    return extra


class DigestError(ArgDigestCatalogException):
    """Base class for all ArgDigest exceptions.

    `message` comes first and every field is keyword-only. That is what makes
    `type(e)(*e.args)` reproduce the instance, which is how `pickle`,
    `copy.deepcopy`, `warnings.warn(text, category)` and pytest-xdist all rebuild
    one. Section 3.3.1 of `SMONITOR_GUIDE.md` explains the failure it prevents.

    Raise sites do **not** pass `message`. They pass typed fields, and the
    catalog template renders the sentence: a message handed over here is used
    verbatim and the template is bypassed entirely, which is what used to happen
    and why four of the templates had never rendered for a user.

        raise DigestTypeError(context=ctx, detail=f"Expected int, got {type(v).__name__}.")

    `detail` is the specific fact the raise site knows and the catalog cannot:
    the framing around it belongs to the template.
    """

    def __init__(
        self,
        message: str | None = None,
        *,
        context: Context | None = None,
        detail: str | None = None,
        code: str | None = None,
        **fields: object,
    ):
        self.context = context
        resolved_code = code or CATALOG["exceptions"][self.catalog_key]["code"]
        # `code`, `message`, `raw_message` and `extra` belong to the catalog base
        # classes, which assign them last from what they are given here.
        super().__init__(
            message,
            code=resolved_code,
            extra=_context_extra(context, detail=detail, **fields),
        )


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
        message: str | None = None,
        *,
        context: Context | None = None,
        detail: str | None = None,
        code: str | None = None,
        **fields: object,
    ):
        self.context = context
        resolved_code = code or CATALOG["warnings"][self.catalog_key]["code"]
        super().__init__(
            message,
            code=resolved_code,
            extra=_context_extra(context, detail=detail, **fields),
        )


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
        message: str | None = None,
        *,
        context: Context | None = None,
        detail: str | None = None,
        code: str | None = None,
        **fields: object,
    ):
        self.context = context
        resolved_code = code or CATALOG["warnings"][self.catalog_key]["code"]
        super().__init__(
            message,
            code=resolved_code,
            extra=_context_extra(context, detail=detail, **fields),
        )


class StandardizerContractError(DigestError):
    """A standardizer that did not honour `(caller, kwargs) -> mapping`.

    Forgetting the `return` is the common case, and without this the failure surfaces
    much later as `AttributeError: 'NoneType' object has no attribute 'items'`, which
    names neither the standardizer nor the library that configured it.
    """

    catalog_key = "StandardizerContractError"
