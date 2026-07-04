import csv
import os
import sqlite3


SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "schema")


def _schema_path(name):
    return os.path.abspath(os.path.join(SCHEMA_DIR, name))


def create_schema(conn):
    path = _schema_path("schema.sql")
    with open(path, encoding="utf-8") as f:
        conn.executescript(f.read())


def _table_columns(conn, table_name):
    cur = conn.execute(f"pragma table_info({table_name})")
    return [row[1] for row in cur.fetchall()]


def import_csvs(conn, csv_paths):
    conn.execute("pragma foreign_keys = 0")
    conn.execute("begin")
    try:
        for table, path in csv_paths.items():
            columns = _table_columns(conn, table)
            placeholders = ", ".join("?" for _ in columns)
            col_list = ", ".join(columns)
            sql = f"insert into {table} ({col_list}) values ({placeholders})"

            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = []
                for row in reader:
                    vals = [row.get(c, "") or None for c in columns]
                    rows.append(vals)
                conn.executemany(sql, rows)
        conn.execute(
            """
            insert or ignore into parts (part_num, name, part_cat_id)
            select child_part_num, parts.name, parts.part_cat_id
            from part_relationships
            join parts on part_num = parent_part_num
            """
        )
        conn.execute(
            """
            insert or ignore into parts (part_num, name, part_cat_id)
            select parent_part_num, parts.name, parts.part_cat_id
            from part_relationships
            join parts on part_num = child_part_num
            """
        )
        conn.execute("commit")
    except Exception:
        conn.execute("rollback")
        raise


def create_indices(conn):
    path = _schema_path("indices.sql")
    with open(path, encoding="utf-8") as f:
        conn.executescript(f.read())


def create_set_lists_table(conn):
    conn.execute(
        """
        create table if not exists set_lists (
            setlist varchar(16),
            set_num varchar(16),
            quantity smallint
        )
        """
    )
    conn.execute("delete from set_lists")