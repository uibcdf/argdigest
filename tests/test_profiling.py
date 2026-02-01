import pytest
import time
from argdigest import digest, register_pipeline

@register_pipeline(kind="slow", name="sleep")
def slow_rule(value, ctx):
    time.sleep(0.01) # 10ms
    return value

def test_profiling_audit_log():
    @digest.map(
        profiling=True,
        val={"kind": "slow", "rules": ["sleep"]}
    )
    def f(val):
        return val

    f(1)
    
    # Check if audit_log is attached to the wrapper
    assert hasattr(f, "audit_log")
    log = f.audit_log
    assert len(log) == 1
    assert log[0]["rule"] == "slow.sleep"
    assert log[0]["duration"] >= 0.01

def test_profiling_disabled_by_default():
    @digest.map(val={"kind": "slow", "rules": ["sleep"]})
    def g(val):
        return val

    g(1)
    assert not hasattr(g, "audit_log")
