import os
import tempfile

import pytest


@pytest.fixture
def tmp_db():
    conn = pytest.importorskip("sqlite3").connect(":memory:")
    yield conn
    conn.close()


@pytest.fixture
def config_dir(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(
            "lego_collection.auth.CONFIG_DIR",
            tmp,
        )
        monkeypatch.setattr(
            "lego_collection.auth.CONFIG_PATH",
            os.path.join(tmp, "lego-collection", "config.ini"),
        )
        yield tmp


@pytest.fixture
def mock_csv_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield tmp