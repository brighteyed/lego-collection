-- lego-collection database verification script
-- Usage: sqlite3 /path/to/database.db < verify.sql

.print \n=== ROW COUNTS ===
select 'themes', count(*) from themes
union all select 'colors', count(*) from colors
union all select 'part_categories', count(*) from part_categories
union all select 'parts', count(*) from parts
union all select 'part_relationships', count(*) from part_relationships
union all select 'elements', count(*) from elements
union all select 'minifigs', count(*) from minifigs
union all select 'sets', count(*) from sets
union all select 'inventories', count(*) from inventories
union all select 'inventory_parts', count(*) from inventory_parts
union all select 'inventory_sets', count(*) from inventory_sets
union all select 'inventory_minifigs', count(*) from inventory_minifigs;

.print \n=== NULL PRIMARY KEYS (should be empty) ===
select 'colors has null id' from colors where id is null
union all select 'parts has null part_num' from parts where part_num is null
union all select 'sets has null set_num' from sets where set_num is null
union all select 'themes has null id' from themes where id is null;

.print \n=== ORPHANED FOREIGN KEY COUNTS ===
.print (small counts are expected — Rebrickable data has gaps for delisted sets)
select 'parts missing category', count(*) from parts p
 where p.part_cat_id is not null
   and p.part_cat_id not in (select id from part_categories)
union all
select 'sets missing theme', count(*) from sets s
 where s.theme_id is not null
   and s.theme_id not in (select id from themes)
union all
select 'inventories missing set', count(*) from inventories i
 where i.set_num not in (select set_num from sets)
union all
select 'elements missing part', count(*) from elements e
 where e.part_num not in (select part_num from parts)
union all
select 'elements missing color', count(*) from elements e
 where e.color_id not in (select id from colors);

.print \n=== SET RANGE ===
select 'Oldest set', min(year) from sets
union all select 'Newest set', max(year) from sets;

.print \n=== YOUR SET LISTS ===
select sl.setlist, sl.set_num, s.name, sl.quantity
  from set_lists sl
  join sets s on s.set_num = sl.set_num
 order by sl.setlist;

.print \n=== SAMPLE: Recent sets with most parts ===
.print (sets with 0 parts are incomplete data and excluded)
select set_num, name, year, num_parts
  from sets
 where year = (select max(year) from sets where num_parts > 0)
   and num_parts > 0
 order by num_parts desc
 limit 10;

.print \n=== SAMPLE: Verify set_parts view ===
select 'set_parts returns rows for ' || set_num, count(*) as parts
  from set_parts
 group by set_num
 order by parts desc
 limit 10;

.print \n=== DONE ===