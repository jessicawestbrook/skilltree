-- Drop unused columns from skill_tree_nodes table
-- Run this in Supabase SQL Editor

-- Drop the columns
ALTER TABLE skill_tree_nodes 
DROP COLUMN IF EXISTS type,
DROP COLUMN IF EXISTS path,
DROP COLUMN IF EXISTS learning_area;

-- Verify the columns were dropped
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'skill_tree_nodes' 
ORDER BY ordinal_position;