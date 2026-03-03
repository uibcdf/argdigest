import importlib.util

import pytest

from argdigest.core.config import DigestConfig, get_defaults, load_from_file, resolve_config, set_defaults


def test_set_defaults_rejects_config_and_kwargs():
    with pytest.raises(ValueError, match="Cannot specify both"):
        set_defaults(config=DigestConfig(), strictness="error")


def test_set_defaults_with_kwargs_updates_defaults():
    original = get_defaults()
    try:
        set_defaults(strictness="error", skip_param="skip_now")
        updated = get_defaults()
        assert updated.strictness == "error"
        assert updated.skip_param == "skip_now"
    finally:
        set_defaults(original)


def test_load_from_file_not_found():
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        load_from_file("this_file_does_not_exist_123.yaml")


def test_load_from_py_file_import_error(monkeypatch, tmp_path):
    cfg_file = tmp_path / "bad_config.py"
    cfg_file.write_text("DIGESTION_STYLE = 'auto'\n")

    monkeypatch.setattr(importlib.util, "spec_from_file_location", lambda *_args, **_kwargs: None)
    with pytest.raises(ImportError, match="Could not load config"):
        load_from_file(cfg_file)


def test_resolve_config_invalid_type():
    with pytest.raises(TypeError, match="config must be a DigestConfig"):
        resolve_config(3.14159)
