import yaml
from argdigest.config import load_from_file
from argdigest import arg_digest, argument_digest

def test_load_from_yaml(tmp_path):
    config_data = {
        "digestion_source": "tests.test_config_file",
        "digestion_style": "decorator",
        "strictness": "error",
        "skip_param": "no_digest"
    }
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)

    cfg = load_from_file(str(config_file))
    
    assert cfg.digestion_style == "decorator"
    assert cfg.strictness == "error"
    assert cfg.skip_param == "no_digest"

def test_digest_with_loaded_config(tmp_path):
    # Setup a decorator-style digester
    @argument_digest("val_yaml")
    def digest_val(val_yaml, caller=None):
        return int(val_yaml) * 10

    config_data = {
        "digestion_style": "decorator",
        "strictness": "ignore"
    }
    config_file = tmp_path / "rules.json"
    import json
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    cfg = load_from_file(str(config_file))

    @arg_digest(config=cfg)
    def f(val_yaml):
        return val_yaml

    assert f("5") == 50
