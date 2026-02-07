import logging
from argdigest import arg_digest
from argdigest.config import setup_logging

@arg_digest(digestion_style="decorator", strictness="ignore")
def sample_func(a):
    return a

def test_logging_output(caplog):
    setup_logging(level=logging.DEBUG)

    with caplog.at_level(logging.DEBUG, logger="argdigest"):
        sample_func("test")

    # Check for start/end logs from decorator
    assert "Digesting arguments for sample_func" in caplog.text