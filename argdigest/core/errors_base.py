from __future__ import annotations

from smonitor.integrations import CatalogException, CatalogWarning
from .._private.smonitor.catalog import CATALOG, META


class ArgDigestCatalogException(CatalogException):
    def __init__(self, **kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        
        super().__init__(catalog=CATALOG, meta=META, **kwargs)

class ArgDigestCatalogWarning(CatalogWarning):
    def __init__(self, **kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        
        super().__init__(catalog=CATALOG, meta=META, **kwargs)
