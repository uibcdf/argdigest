import pytest

from argdigest.core.argument_registry import ArgumentRegistry


@pytest.fixture(autouse=True)
def _clear_argument_registry():
    from argdigest.core.config import DigestConfig, set_defaults

    ArgumentRegistry.clear()
    set_defaults(DigestConfig())
    yield
    ArgumentRegistry.clear()
    set_defaults(DigestConfig())
