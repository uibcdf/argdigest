import logging
import pytest
from argdigest import digest, register_pipeline
from argdigest.config import setup_logging

@register_pipeline(kind="log_test", name="noop")
def noop(value, ctx):
    return value

@digest.map(a={"kind": "log_test", "rules": ["noop", "missing_rule"]})
def sample_func(a):
    return a

def test_logging_output(caplog):
    setup_logging(level=logging.DEBUG)
    
    with caplog.at_level(logging.DEBUG, logger="argdigest"):
        sample_func("test")

    # Check for start/end logs from decorator
    assert "Digesting arguments for test_logging.sample_func" in caplog.text
    assert "Digestion complete for test_logging.sample_func" in caplog.text
    
    # Check for pipeline logs
    assert "Starting pipelines for kind='log_test' on argument='a'" in caplog.text
    assert "Running rule 'log_test.noop' on argument='a'" in caplog.text
    
    # Check for warning on missing rule
    assert "Rule 'missing_rule' not found for kind='log_test'. Skipping." in caplog.text
