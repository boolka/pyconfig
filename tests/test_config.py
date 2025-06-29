from pyconfig.config import Config
from os import environ


def test_config():
    environ["TEST_FILE_ENV"] = "env.toml"

    config = Config("./tests/testdata/config", "testing", 1, "host-name")
    config.init()

    assert config.get("default") == "default.json"
    assert config.get("default-1") == "default-1.json"
    assert config.get("testing") == "testing.toml"
    assert config.get("testing-1") == "testing-1.toml"
    assert config.get("host-name") == "host-name.toml"
    assert config.get("host-name-1") == "host-name-1.toml"
    assert config.get("local") == "local.toml"
    assert config.get("local-1") == "local-1.toml"
    assert config.get("local-testing") == "local-testing.toml"
    assert config.get("local-testing-1") == "local-testing-1.toml"
    assert config.get("env") == "env.toml"

    assert config.get("unknown.path") is None
