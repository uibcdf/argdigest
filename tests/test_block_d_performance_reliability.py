from __future__ import annotations

import json
import subprocess
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from argdigest import arg_digest, argument_digest, register_pipeline
from argdigest.core import decorator as decorator_mod
from argdigest.core.registry import Registry


def test_signature_metadata_cache_reused_under_repeated_calls(monkeypatch):
    decorator_mod._DIGESTER_METADATA_CACHE.clear()
    call_counter = {"n": 0}
    original_signature = decorator_mod.inspect.signature

    def counting_signature(obj):
        if getattr(obj, "__name__", "") == "digest_cache_arg":
            call_counter["n"] += 1
        return original_signature(obj)

    monkeypatch.setattr(decorator_mod.inspect, "signature", counting_signature)

    @argument_digest("cache_arg")
    def digest_cache_arg(cache_arg, caller=None):
        return int(cache_arg)

    @arg_digest(digestion_style="decorator", strictness="ignore")
    def f(cache_arg):
        return cache_arg

    for _ in range(200):
        assert f("7") == 7

    assert call_counter["n"] == 1


def test_decorator_overhead_with_disabled_digestion_stays_bounded(monkeypatch):
    monkeypatch.delenv("ARGDIGEST_CONFIG", raising=False)

    def plain(x):
        return x + 1

    @arg_digest()
    def digested(x):
        return x + 1

    for _ in range(1000):
        plain(1)
        digested(1)

    loops = 30000
    start = time.perf_counter()
    for _ in range(loops):
        plain(1)
    plain_elapsed = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(loops):
        digested(1)
    digested_elapsed = time.perf_counter() - start

    per_call = digested_elapsed / loops
    assert per_call < 0.0004


def test_import_time_is_lightweight_and_does_not_load_optional_stacks():
    snippet = (
        "import json, sys, time;"
        "t=time.perf_counter();"
        "import argdigest;"
        "elapsed=time.perf_counter()-t;"
        "print(json.dumps({"
        "'elapsed': elapsed,"
        "'version': getattr(argdigest,'__version__',''),"
        "'beartype_loaded': 'beartype' in sys.modules,"
        "'pydantic_loaded': 'pydantic' in sys.modules,"
        "'pyunitwizard_loaded': 'pyunitwizard' in sys.modules"
        "}))"
    )
    proc = subprocess.run(
        [sys.executable, "-c", snippet],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(proc.stdout.strip().splitlines()[-1])

    assert payload["elapsed"] < 2.0
    assert payload["version"]
    assert payload["beartype_loaded"] is False
    assert payload["pydantic_loaded"] is False
    assert payload["pyunitwizard_loaded"] is False


def test_registry_and_digestion_are_read_safe_under_threads():
    kind = f"thread_kind_{uuid.uuid4().hex}"

    def make_rule(delta):
        def _rule(value, _ctx):
            return value + delta

        return _rule

    with ThreadPoolExecutor(max_workers=8) as executor:
        for idx in range(50):
            executor.submit(register_pipeline(kind, f"r{idx}"), make_rule(idx))

    assert len(Registry.get_pipelines(kind)) == 50

    @argument_digest("thread_a")
    def digest_thread_a(thread_a, caller=None):
        return int(thread_a) + 1

    @arg_digest(digestion_style="decorator", strictness="ignore")
    def f(thread_a):
        return thread_a

    with ThreadPoolExecutor(max_workers=8) as executor:
        outputs = list(executor.map(lambda x: f(str(x)), range(200)))

    assert outputs[0] == 1
    assert outputs[-1] == 200
