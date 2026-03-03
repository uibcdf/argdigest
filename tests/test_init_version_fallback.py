import importlib
import importlib.metadata as importlib_metadata


def test_init_uses_local_version_fallback_when_metadata_missing(monkeypatch):
    import argdigest
    import argdigest._version as local_version

    with monkeypatch.context() as m:
        def _raise_package_not_found(_name):
            raise importlib_metadata.PackageNotFoundError

        m.setattr(importlib_metadata, "version", _raise_package_not_found)
        reloaded = importlib.reload(argdigest)
        assert reloaded.__version__ == local_version.__version__

    # Restore normal importlib.metadata.version behavior for following tests.
    importlib.reload(argdigest)
