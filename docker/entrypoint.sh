#!/bin/sh
# Build the database into the data directory.
set -e

DB_PATH="${DB_PATH:-/data/bricks.db}"

mkdir -p "$(dirname "$DB_PATH")"

lego-collection build --db "$DB_PATH"
