-- Add description column to skill_tree_nodes table
-- This column will store generated descriptions for categories

ALTER TABLE skill_tree_nodes 
ADD COLUMN description TEXT;

-- Add a comment to document the column purpose
COMMENT ON COLUMN skill_tree_nodes.description IS 'AI-generated description of the category or skill area';

-- Verify the column was added
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'skill_tree_nodes' 
  AND column_name = 'description';