import os
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_numpy_is_only_an_optional_science_dependency():
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = metadata["project"]

    assert not any(item.startswith("numpy") for item in project["dependencies"])
    assert any(
        item.startswith("numpy") for item in project["optional-dependencies"]["science"]
    )


def test_core_import_and_standard_pipeline_do_not_load_numpy():
    script = """
import builtins
import sys

original_import = builtins.__import__
def without_numpy(name, *args, **kwargs):
    if name == 'numpy' or name.startswith('numpy.'):
        raise ImportError('numpy deliberately unavailable')
    return original_import(name, *args, **kwargs)
builtins.__import__ = without_numpy

import argdigest
from argdigest.pipelines.coercers import to_bool
from argdigest.pipelines.science import to_quantity_array

assert 'numpy' not in sys.modules
assert to_bool('yes') is True
try:
    to_quantity_array([1, 2])
except ImportError as error:
    assert 'argdigest[science]' in str(error)
else:
    raise AssertionError('scientific pipeline accepted absent numpy')
"""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT)

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
