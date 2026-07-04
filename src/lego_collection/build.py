import sqlite3
import tempfile

from . import api
from . import auth as auth_mod
from . import downloader
from . import importer


def build(db_path):
    config = auth_mod.read_config()
    api_key = config["api_key"]
    username = config["username"]
    password = config["password"]

    print("Downloading Rebrickable CSV dumps...")
    with tempfile.TemporaryDirectory(prefix="lego-collection-") as tmpdir:
        csv_paths = downloader.download_csvs(tmpdir)

        print("Building database...")
        conn = sqlite3.connect(db_path)
        conn.execute("pragma journal_mode = off")
        conn.execute("pragma synchronous = off")
        try:
            print("  Creating schema...")
            importer.create_schema(conn)

            print("  Importing data...")
            importer.import_csvs(conn, csv_paths)

            print("  Creating indices...")
            importer.create_indices(conn)

            print("Fetching set lists from Rebrickable API...")
            user_token = api.get_user_token(api_key, username, password)
            set_lists = api.get_set_lists(user_token, api_key)

            importer.create_set_lists_table(conn)
            conn.execute("begin")
            try:
                count = 0
                for sl in set_lists:
                    list_id = sl["id"]
                    sets = api.get_list_sets(user_token, list_id, api_key)
                    rows = [
                        (s["list_id"], s["set"]["set_num"], s["quantity"])
                        for s in sets
                    ]
                    conn.executemany(
                        "insert into set_lists values (?, ?, ?)", rows
                    )
                    count += len(rows)
                conn.execute("commit")
                print(f"  Inserted {count} set list entries.")
            except Exception:
                conn.execute("rollback")
                raise

        finally:
            conn.close()

    print(f"Database written to {db_path}")