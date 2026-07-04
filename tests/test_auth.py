import os

from lego_collection import auth as auth_mod


def test_write_and_read_config(config_dir):
    auth_mod.write_config("key123", "user1", "pass1")
    result = auth_mod.read_config()
    assert result == {"api_key": "key123", "username": "user1", "password": "pass1"}
    assert os.path.exists(auth_mod.CONFIG_PATH)


def test_read_config_missing_file(config_dir):
    with pytest.raises(FileNotFoundError, match="lego-collection auth"):
        auth_mod.read_config()


def test_read_config_missing_section(config_dir):
    os.makedirs(os.path.dirname(auth_mod.CONFIG_PATH), exist_ok=True)
    with open(auth_mod.CONFIG_PATH, "w") as f:
        f.write("[other]\nkey = val\n")
    with pytest.raises(KeyError, match="Missing section"):
        auth_mod.read_config()


def test_read_config_empty_value(config_dir):
    auth_mod.write_config("key123", "", "pass1")
    with pytest.raises(KeyError, match="username"):
        auth_mod.read_config()


import pytest