create index if not exists inventories_set_num_idx on inventories (set_num);
create index if not exists inventory_parts_inventory_id_idx on inventory_parts (inventory_id);
create index if not exists inventory_parts_part_num_idx on inventory_parts (part_num);
create index if not exists inventory_parts_color_id_idx on inventory_parts (color_id);
create index if not exists inventory_parts_part_num_color_id_idx on inventory_parts (part_num, color_id);