-- Add skill_node_id to learning_paths table to associate courses with skills

-- First, create a backup of the learning_paths table
CREATE TABLE IF NOT EXISTS learning_paths_bkp AS 
SELECT * FROM learning_paths;

-- Add the skill_node_id column to learning_paths table
ALTER TABLE learning_paths 
ADD COLUMN IF NOT EXISTS skill_node_id UUID REFERENCES skill_tree_nodes(id) ON DELETE SET NULL;

-- Create an index for better query performance
CREATE INDEX IF NOT EXISTS idx_learning_paths_skill_node_id ON learning_paths(skill_node_id);

-- Add a comment to document the field
COMMENT ON COLUMN learning_paths.skill_node_id IS 'References the skill tree node this learning path is associated with';

-- Verify the column was added
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'learning_paths' 
AND column_name = 'skill_node_id';

-- Show current learning paths to verify
SELECT id, name, skill_node_id FROM learning_paths;