import gzip
import os
import requests


CDN_BASE = "https://cdn.rebrickable.com/media/downloads"

TABLES = [
    "themes",
    "colors",
    "part_categories",
    "parts",
    "part_relationships",
    "elements",
    "minifigs",
    "sets",
    "inventories",
    "inventory_parts",
    "inventory_sets",
    "inventory_minifigs",
]


def download_csvs(target_dir):
    paths = {}
    for table in TABLES:
        url = f"{CDN_BASE}/{table}.csv.gz"
        dest = os.path.join(target_dir, f"{table}.csv")
        print(f"  Downloading {table}...")
        try:
            resp = requests.get(url, stream=True, timeout=300)
            resp.raise_for_status()
            data = gzip.decompress(resp.content)
            lines = data.decode("utf-8").splitlines()
            with open(dest, "w", encoding="utf-8") as f:
                f.writelines(line + "\n" for line in lines)
            paths[table] = dest
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to download {table}: {e}") from e
        except (gzip.BadGzipFile, UnicodeDecodeError) as e:
            raise RuntimeError(f"Failed to decompress {table}: {e}") from e
    return paths