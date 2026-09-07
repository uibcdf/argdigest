from __future__ import annotations

from smonitor.integrations import CatalogException, CatalogWarning

from .._private.smonitor.catalog import CATALOG, META


class ArgDigestCatalogException(CatalogException):
    """Binds every ArgDigest exception to this package's catalog and metadata.

    `message` is positional-or-keyword, as section 3.3.1 of `SMONITOR_GUIDE.md`
    requires: Python rebuilds an exception as `type(e)(*e.args)`, and a
    keyword-only signature makes that call -- and `warnings.warn(text, category)`,
    which uses it -- fail with `TypeError`.
    """

    def __init__(self, message: str | None = None, **kwargs: object):
        kwargs.setdefault("extra", {})
        super().__init__(message, catalog=CATALOG, meta=META, **kwargs)


class ArgDigestCatalogWarning(CatalogWarning):
    """The warning half of the same binding. See above for why `message` is first."""

    def __init__(self, message: str | None = None, **kwargs: object):
        kwargs.setdefault("extra", {})
        super().__init__(message, catalog=CATALOG, meta=META, **kwargs)
