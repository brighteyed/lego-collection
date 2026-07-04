# AGENTS.md — for AI coding assistants

## Build / install

```bash
pip install -e ".[test]"      # editable install with test deps
pipx install .                # production install via pipx
```

## Run tests

```bash
pytest -v                     # all tests
pytest tests/test_schema.py   # single file
```

## CLI

```bash
lego-collection auth          # store Rebrickable credentials
lego-collection build --db bricks.db  # build database
sqlite3 bricks.db < verify.sql  # verify DB integrity
python -m lego_collection     # alternative entry point
```

## Project structure

```
src/lego_collection/   # package source
  cli.py               # argparse entry point (auth / build subcommands)
  auth.py              # config file read/write (configparser, INI format)
  build.py             # orchestrator: download → import → patch
  downloader.py        # fetch .csv.gz from cdn.rebrickable.com
  importer.py          # schema creation, CSV import, indices
  api.py               # Rebrickable v3 API client (auth + set lists)
schema/                # SQL files shipped as package data
  schema.sql           # 11 tables + 5 views (DROP-before-CREATE)
  indices.sql          # 5 indices
verify.sql             # standalone DB verification script
tests/                 # pytest tests with mocked HTTP / in-memory SQLite
```

## Conventions

- Uses `requests`, stdlib only otherwise (`sqlite3`, `csv`, `argparse`, `configparser`, `gzip`, `tempfile`, `getpass`)
- Credentials stored in `~/.config/lego-collection/config.ini` (Linux/Mac) or `%APPDATA%\lego-collection\config.ini` (Windows)
- No Docker, no make, no external tools
- Empty CSV fields are converted to `NULL` during import