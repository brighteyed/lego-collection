import configparser
import os
import sys


CONFIG_DIR = (
    os.environ.get("APPDATA", os.path.expanduser("~"))
    if sys.platform == "win32"
    else os.environ.get(
        "XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config")
    )
)
CONFIG_PATH = os.path.join(CONFIG_DIR, "lego-collection", "config.ini")

SECTION = "rebrickable"
KEYS = ["api_key", "username", "password"]

ENV_VARS = {
    "api_key": "REBRICKABLE_API_KEY",
    "username": "REBRICKABLE_USERNAME",
    "password": "REBRICKABLE_PASSWORD",
}


def write_config(api_key, username, password):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    config = configparser.ConfigParser()
    config[SECTION] = {"api_key": api_key, "username": username, "password": password}
    with open(CONFIG_PATH, "w") as f:
        config.write(f)
    try:
        os.chmod(CONFIG_PATH, 0o600)
    except OSError:
        pass


def read_config():
    env = {
        key: os.environ.get(var, "").strip()
        for key, var in ENV_VARS.items()
    }
    if all(env.values()):
        return env
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            "No credentials found: set REBRICKABLE_API_KEY, REBRICKABLE_USERNAME "
            "and REBRICKABLE_PASSWORD (see .env.example), or run "
            f"'lego-collection auth' to create {CONFIG_PATH}."
        )
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    if SECTION not in config:
        raise KeyError(f"Missing section [{SECTION}] in {CONFIG_PATH}")
    result = {}
    for key in KEYS:
        value = config[SECTION].get(key, "").strip()
        if not value:
            raise KeyError(f"Missing '{key}' in [{SECTION}] section of {CONFIG_PATH}")
        result[key] = value
    return result