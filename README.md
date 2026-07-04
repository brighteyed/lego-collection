# lego-collection

Creates a local SQLite database combining the public [Rebrickable](https://rebrickable.com) LEGO database with your personal set lists.

## Installation

Requires Python 3.9+.

```bash
pipx install .
```

Or with pip in a virtual environment:

```bash
pip install .
```

## Build the database

### 1. Store your Rebrickable credentials

```bash
lego-collection auth
```

You'll be prompted for your Rebrickable API key, username, and password. Credentials are saved to a config file:

- **Linux/Mac**: `~/.config/lego-collection/config.ini`
- **Windows**: `%APPDATA%\lego-collection\config.ini`

### 2. Build the database

```bash
lego-collection build
```

This downloads the latest CSV dumps from Rebrickable (themes, colors, parts, sets, inventories, etc.), creates a SQLite database with indices and views, then appends your personal set lists from the Rebrickable API.

The output is written to `bricks.db` in the current directory. Use `--db` to specify a different path:

```bash
lego-collection build --db ~/lego/bricks.db
```

## Query the database

Use any SQLite client:

```bash
sqlite3 bricks.db
```

```sql
-- Colors
SELECT id, name FROM colors LIMIT 5;

-- Parts in a set
SELECT part_num, color_id, quantity
FROM set_parts
WHERE set_num = '10193-1'
LIMIT 5;

-- Your personal set lists
SELECT * FROM set_lists;
```

See `examples.sql` in the upstream [rebrickable-sqlite](https://github.com/jncraton/rebrickable-sqlite) repository for more query examples.

## Verify the database

Run the included script to check row counts, detect null primary keys and orphaned foreign keys, and preview your set lists:

```bash
sqlite3 bricks.db < verify.sql
```

Sample output:

```
=== ROW COUNTS ===
colors|275
parts|108632
sets|26285
...

=== NULL PRIMARY KEYS (should be empty) ===
=== ORPHANED FOREIGN KEY COUNTS ===
(small counts are expected — Rebrickable data has gaps for delisted sets)
parts missing category|0
sets missing theme|0
inventories missing set|17031
elements missing part|2
elements missing color|0

=== YOUR SET LISTS ===
mylist|10193-1|Medieval Market Village|1
```

Small orphan counts are normal (delisted sets in Rebrickable data). Non-zero counts in the NULL checks would indicate a real problem.

## How it works

1. **Downloads** 12 compressed CSV files from `cdn.rebrickable.com`
2. **Creates** 11 tables (`themes`, `colors`, `parts`, `sets`, `inventories`, etc.) and 5 views (`set_parts`, `part_info`, `part_color_info`, `part_nums`, `canonical_parts`)
3. **Imports** all CSV data into the database
4. **Creates** indices on commonly queried columns
5. **Authenticates** against the Rebrickable API v3 and fetches your set lists
6. **Appends** a `set_lists` table with your personal collection data

## Testing

```bash
# Install with test dependencies
pip install -e ".[test]"

# Run tests
pytest

# Run with verbose output
pytest -v
```

The test suite covers:
- **Schema** — all 11 tables, 5 views, and 5 indices are created correctly; schema can be rebuilt idempotently
- **CSV import** — data round-trips correctly, extra CSV columns are ignored, relationship parts are expanded
- **API client** — authentication, pagination, and set list fetching (with mocked HTTP)
- **Config** — config file write/read, missing file error, missing keys

## Acknowledgments

- [Rebrickable](https://rebrickable.com) for providing the public LEGO database and API.
- [jncraton/rebrickable-sqlite](https://github.com/jncraton/rebrickable-sqlite) for the SQL schema and query patterns that inspired the database layout.

## License

MIT