import os

import pytest

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


def test_read_config_from_env(monkeypatch):
    monkeypatch.setenv("REBRICKABLE_API_KEY", "key123")
    monkeypatch.setenv("REBRICKABLE_USERNAME", "user1")
    monkeypatch.setenv("REBRICKABLE_PASSWORD", "pass1")
    result = auth_mod.read_config()
    assert result == {"api_key": "key123", "username": "user1", "password": "pass1"}


def test_read_config_partial_env_falls_back_to_file(monkeypatch, config_dir):
    monkeypatch.setenv("REBRICKABLE_API_KEY", "key123")
    monkeypatch.delenv("REBRICKABLE_USERNAME", raising=False)
    monkeypatch.delenv("REBRICKABLE_PASSWORD", raising=False)
    auth_mod.write_config("key456", "user2", "pass2")
    result = auth_mod.read_config()
    assert result == {"api_key": "key456", "username": "user2", "password": "pass2"}


def test_read_config_env_hint_in_missing_file_error(monkeypatch, config_dir):
    monkeypatch.delenv("REBRICKABLE_API_KEY", raising=False)
    monkeypatch.delenv("REBRICKABLE_USERNAME", raising=False)
    monkeypatch.delenv("REBRICKABLE_PASSWORD", raising=False)
    with pytest.raises(FileNotFoundError, match="REBRICKABLE_API_KEY"):
        auth_mod.read_config()