import sqlite3

import pytest

from lego_collection import importer

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

VIEWS = [
    "set_parts",
    "part_info",
    "part_color_info",
    "part_nums",
    "canonical_parts",
]

INDICES = [
    "inventories_set_num_idx",
    "inventory_parts_inventory_id_idx",
    "inventory_parts_part_num_idx",
    "inventory_parts_color_id_idx",
    "inventory_parts_part_num_color_id_idx",
]


def test_tables_exist(tmp_db):
    importer.create_schema(tmp_db)
    cur = tmp_db.execute(
        "select name from sqlite_master where type='table' order by name"
    )
    names = [row[0] for row in cur]
    for t in TABLES:
        assert t in names, f"Missing table: {t}"


def test_views_exist(tmp_db):
    importer.create_schema(tmp_db)
    cur = tmp_db.execute(
        "select name from sqlite_master where type='view' order by name"
    )
    names = [row[0] for row in cur]
    for v in VIEWS:
        assert v in names, f"Missing view: {v}"


def test_indices_exist(tmp_db):
    importer.create_schema(tmp_db)
    importer.create_indices(tmp_db)
    cur = tmp_db.execute(
        "select name from sqlite_master where type='index' and name != 'sqlite_autoindex_*' order by name"
    )
    names = [row[0] for row in cur]
    for idx in INDICES:
        assert idx in names, f"Missing index: {idx}"


def test_themes_columns(tmp_db):
    importer.create_schema(tmp_db)
    cur = tmp_db.execute("pragma table_info(themes)")
    cols = {row[1] for row in cur}
    assert cols == {"id", "name", "parent_id"}


def test_parts_columns(tmp_db):
    importer.create_schema(tmp_db)
    cur = tmp_db.execute("pragma table_info(parts)")
    cols = {row[1] for row in cur}
    assert cols == {"part_num", "name", "part_cat_id", "part_material_id"}


def test_set_lists_table(tmp_db):
    importer.create_set_lists_table(tmp_db)
    cur = tmp_db.execute("pragma table_info(set_lists)")
    cols = {row[1] for row in cur}
    assert cols == {"setlist", "set_num", "quantity"}