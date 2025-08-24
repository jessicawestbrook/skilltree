-- Alternative simpler approach if the above doesn't work
-- This assigns display_order to any NULL values, preserving existing ones

-- First check what we're dealing with
SELECT 
  COUNT(*) as nodes_without_display_order,
  COUNT(DISTINCT parent_id) as unique_parents
FROM skill_tree_nodes
WHERE display_order IS NULL;

-- Simple update: assign sequential numbers starting from max existing + 1 for each parent
UPDATE skill_tree_nodes n1
SET display_order = (
  SELECT COUNT(*) + 1
  FROM skill_tree_nodes n2
  WHERE n2.parent_id IS NOT DISTINCT FROM n1.parent_id
    AND n2.display_order IS NOT NULL
) + (
  SELECT COUNT(*)
  FROM skill_tree_nodes n3
  WHERE n3.parent_id IS NOT DISTINCT FROM n1.parent_id
    AND n3.display_order IS NULL
    AND n3.id < n1.id
)
WHERE n1.display_order IS NULL;

-- If the above is too complex, here's an even simpler version:
-- Just assign any number to nodes that don't have one
UPDATE skill_tree_nodes
SET display_order = 999
WHERE display_order IS NULL;

-- Then fix them with proper sequential numbering
WITH numbered AS (
  SELECT 
    id,
    ROW_NUMBER() OVER (PARTITION BY parent_id ORDER BY name) as rn
  FROM skill_tree_nodes
  WHERE display_order = 999
)
UPDATE skill_tree_nodes
SET display_order = numbered.rn + COALESCE((
  SELECT MAX(display_order) 
  FROM skill_tree_nodes s2 
  WHERE s2.parent_id IS NOT DISTINCT FROM skill_tree_nodes.parent_id
    AND s2.display_order != 999
), 0)
FROM numbered
WHERE skill_tree_nodes.id = numbered.id;

-- Final check
SELECT 
  COUNT(*) as total,
  COUNT(display_order) as with_display_order,
  COUNT(CASE WHEN display_order IS NULL THEN 1 END) as without_display_order
FROM skill_tree_nodes;