-- Remove type column from skill_tree_nodes table
-- This script safely removes the type column after backing up the data

-- First, create a backup table with the type data in case we need to restore it
CREATE TABLE skill_tree_nodes_type_backup AS 
SELECT id, type FROM skill_tree_nodes;

-- Add comment to backup table
COMMENT ON TABLE skill_tree_nodes_type_backup IS 'Backup of type column data before removal - created on 2025-08-21';

-- Verify backup was created
SELECT COUNT(*) as backup_count FROM skill_tree_nodes_type_backup;

-- Now remove the type column from the main table
ALTER TABLE skill_tree_nodes DROP COLUMN type;

-- Verify the column was removed
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'skill_tree_nodes' 
  AND column_name = 'type';