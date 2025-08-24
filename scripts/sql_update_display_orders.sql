-- SQL script to update display_order for all nodes without it
-- Run this in Supabase SQL Editor

-- First, create a backup table (if not already created)
CREATE TABLE IF NOT EXISTS skill_tree_nodes_bkp_2025_01_24 AS 
SELECT * FROM skill_tree_nodes;

-- Update display_order for nodes grouped by parent_id
-- This uses ROW_NUMBER() to assign sequential numbers within each parent group

WITH ordered_nodes AS (
  SELECT 
    id,
    parent_id,
    name,
    ROW_NUMBER() OVER (
      PARTITION BY parent_id 
      ORDER BY 
        -- Academic ordering logic
        CASE 
          -- Languages
          WHEN name LIKE '%Spanish%' THEN 1
          WHEN name LIKE '%French%' THEN 2
          WHEN name LIKE '%German%' THEN 3
          WHEN name LIKE '%Italian%' THEN 4
          WHEN name LIKE '%Portuguese%' THEN 5
          WHEN name LIKE '%Chinese%' THEN 6
          WHEN name LIKE '%Japanese%' THEN 7
          WHEN name LIKE '%Korean%' THEN 8
          WHEN name LIKE '%Arabic%' THEN 9
          WHEN name LIKE '%Russian%' THEN 10
          WHEN name LIKE '%Latin%' THEN 15
          WHEN name LIKE '%Ancient Greek%' THEN 20
          -- Math levels
          WHEN name LIKE '%Early%' THEN 1
          WHEN name LIKE '%Elementary%' THEN 2
          WHEN name LIKE '%Basic%' THEN 3
          WHEN name LIKE '%Pre-Algebra%' THEN 4
          WHEN name LIKE '%Algebra%' AND name NOT LIKE '%Pre-%' AND name NOT LIKE '%Abstract%' THEN 5
          WHEN name LIKE '%Geometry%' THEN 6
          WHEN name LIKE '%Trigonometry%' THEN 7
          WHEN name LIKE '%Pre-Calculus%' THEN 8
          WHEN name LIKE '%Calculus%' AND name NOT LIKE '%Pre-%' THEN 9
          WHEN name LIKE '%Statistics%' THEN 10
          WHEN name LIKE '%Differential%' THEN 11
          WHEN name LIKE '%Abstract%' THEN 15
          WHEN name LIKE '%Advanced%' THEN 20
          -- Sciences
          WHEN name LIKE '%Biology%' THEN 1
          WHEN name LIKE '%Chemistry%' THEN 2
          WHEN name LIKE '%Physics%' THEN 3
          WHEN name LIKE '%Earth Science%' THEN 4
          WHEN name LIKE '%Environmental%' THEN 5
          WHEN name LIKE '%Astronomy%' THEN 6
          -- History periods
          WHEN name LIKE '%Ancient%' THEN 1
          WHEN name LIKE '%Classical%' THEN 2
          WHEN name LIKE '%Medieval%' THEN 3
          WHEN name LIKE '%Renaissance%' THEN 4
          WHEN name LIKE '%Modern%' THEN 5
          WHEN name LIKE '%Contemporary%' THEN 6
          -- Grade levels
          WHEN name LIKE '%Kindergarten%' THEN 1
          WHEN name LIKE '%First%' THEN 2
          WHEN name LIKE '%Second%' THEN 3
          WHEN name LIKE '%Third%' THEN 4
          WHEN name LIKE '%Fourth%' THEN 5
          WHEN name LIKE '%Fifth%' THEN 6
          WHEN name LIKE '%Sixth%' THEN 7
          WHEN name LIKE '%Seventh%' THEN 8
          WHEN name LIKE '%Eighth%' THEN 9
          WHEN name LIKE '%Ninth%' THEN 10
          WHEN name LIKE '%Tenth%' THEN 11
          WHEN name LIKE '%Eleventh%' THEN 12
          WHEN name LIKE '%Twelfth%' THEN 13
          ELSE 100
        END,
        name -- Secondary sort alphabetically
    ) AS new_display_order
  FROM skill_tree_nodes
  WHERE display_order IS NULL
)
UPDATE skill_tree_nodes
SET display_order = ordered_nodes.new_display_order
FROM ordered_nodes
WHERE skill_tree_nodes.id = ordered_nodes.id;

-- Verify the update
SELECT 
  COUNT(*) as total_nodes,
  COUNT(display_order) as nodes_with_display_order,
  COUNT(*) - COUNT(display_order) as nodes_without_display_order
FROM skill_tree_nodes;

-- Show some examples of the updated ordering
SELECT 
  name,
  parent_id,
  display_order
FROM skill_tree_nodes
WHERE display_order IS NOT NULL
ORDER BY parent_id, display_order
LIMIT 50;