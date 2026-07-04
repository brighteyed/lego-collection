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
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"No credentials found at {CONFIG_PATH}. Run 'lego-collection auth' first."
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