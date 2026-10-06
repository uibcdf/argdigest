import pytest

from argdigest.core.argument_registry import ArgumentRegistry


def pytest_addoption(parser):
    parser.addoption(
        "--require-scoped-capture",
        action="store_true",
        help="Fail instead of skipping scoped capture in the installed release gate.",
    )


@pytest.fixture(autouse=True)
def _clear_argument_registry():
    from argdigest.core.config import DigestConfig, set_defaults

    ArgumentRegistry.clear()
    set_defaults(DigestConfig())
    yield
    ArgumentRegistry.clear()
    set_defaults(DigestConfig())
