import csv
import os

import pytest

from lego_collection import importer


def _write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def test_import_colors(tmp_db, mock_csv_dir):
    importer.create_schema(tmp_db)
    path = os.path.join(mock_csv_dir, "colors.csv")
    _write_csv(path, ["id", "name", "rgb", "is_trans"], [
        {"id": "1", "name": "Blue", "rgb": "0055BF", "is_trans": "f"},
        {"id": "2", "name": "Red", "rgb": "C91A09", "is_trans": "f"},
    ])
    importer.import_csvs(tmp_db, {"colors": path})
    cur = tmp_db.execute("select id, name from colors order by id")
    rows = cur.fetchall()
    assert rows == [(1, "Blue"), (2, "Red")]


def test_import_parts_with_category(tmp_db, mock_csv_dir):
    importer.create_schema(tmp_db)
    cat_path = os.path.join(mock_csv_dir, "part_categories.csv")
    _write_csv(cat_path, ["id", "name"], [
        {"id": "1", "name": "Bricks"},
    ])
    parts_path = os.path.join(mock_csv_dir, "parts.csv")
    _write_csv(parts_path, ["part_num", "name", "part_cat_id", "part_material_id"], [
        {"part_num": "3001", "name": "Brick 2x4", "part_cat_id": "1", "part_material_id": ""},
    ])
    importer.import_csvs(tmp_db, {"part_categories": cat_path, "parts": parts_path})
    cur = tmp_db.execute("select part_num, name, part_cat_id from parts")
    assert cur.fetchall() == [("3001", "Brick 2x4", 1)]


def test_import_extra_columns(tmp_db, mock_csv_dir):
    importer.create_schema(tmp_db)
    path = os.path.join(mock_csv_dir, "themes.csv")
    _write_csv(path, ["id", "name", "parent_id", "extra_col"], [
        {"id": "1", "name": "City", "parent_id": "", "extra_col": "ignored"},
    ])
    importer.import_csvs(tmp_db, {"themes": path})
    cur = tmp_db.execute("select id, name, parent_id from themes")
    assert cur.fetchall() == [(1, "City", None)]


def test_part_relationship_expansion(tmp_db, mock_csv_dir):
    importer.create_schema(tmp_db)
    cat_path = os.path.join(mock_csv_dir, "part_categories.csv")
    _write_csv(cat_path, ["id", "name"], [{"id": 1, "name": "Bricks"}])
    parts_path = os.path.join(mock_csv_dir, "parts.csv")
    _write_csv(parts_path, ["part_num", "name", "part_cat_id", "part_material_id"], [
        {"part_num": "3001", "name": "Brick 2x4", "part_cat_id": "1", "part_material_id": ""},
    ])
    rel_path = os.path.join(mock_csv_dir, "part_relationships.csv")
    _write_csv(rel_path, ["rel_type", "child_part_num", "parent_part_num"], [
        {"rel_type": "A", "child_part_num": "3001a", "parent_part_num": "3001"},
    ])
    importer.import_csvs(tmp_db, {
        "part_categories": cat_path,
        "parts": parts_path,
        "part_relationships": rel_path,
    })
    cur = tmp_db.execute("select part_num from parts order by part_num")
    part_nums = [row[0] for row in cur]
    assert "3001a" in part_nums


def test_set_lists_insert(tmp_db):
    importer.create_set_lists_table(tmp_db)
    tmp_db.execute(
        "insert into set_lists values (?, ?, ?)",
        ("list1", "10193-1", 1),
    )
    cur = tmp_db.execute("select * from set_lists")
    assert cur.fetchall() == [("list1", "10193-1", 1)]


def test_set_lists_cleared_on_recreate(tmp_db):
    importer.create_set_lists_table(tmp_db)
    tmp_db.execute("insert into set_lists values ('a', 'b', 1)")
    importer.create_set_lists_table(tmp_db)
    cur = tmp_db.execute("select count(*) from set_lists")
    assert cur.fetchone()[0] == 0