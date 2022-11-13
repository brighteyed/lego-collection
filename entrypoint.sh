#!/bin/sh

make --always-make --directory=/bricks/rebrickable &&
python /bricks/setlists/setlists.py /bricks/rebrickable/dist/bricks.db &&
cp /bricks/rebrickable/dist/bricks.db /database/bricks.db

