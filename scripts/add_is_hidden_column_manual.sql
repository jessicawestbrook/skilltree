-- Add is_hidden column to skill_tree_nodes table
-- Run this in Supabase SQL Editor

-- Step 1: Add the column
ALTER TABLE skill_tree_nodes 
ADD COLUMN IF NOT EXISTS is_hidden BOOLEAN DEFAULT FALSE;

-- Step 2: Create index for performance
CREATE INDEX IF NOT EXISTS idx_skill_tree_nodes_is_hidden 
ON skill_tree_nodes(is_hidden);

-- Step 3: Add comment for documentation
COMMENT ON COLUMN skill_tree_nodes.is_hidden IS 'When true, hides this node and all its descendants from non-admin users';

-- Step 4: Create a function to get all visible nodes (considering parent visibility)
CREATE OR REPLACE FUNCTION get_visible_nodes()
RETURNS SETOF skill_tree_nodes AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE visible_tree AS (
        -- Start with root nodes that are not hidden
        SELECT * FROM skill_tree_nodes
        WHERE parent_id IS NULL AND (is_hidden = FALSE OR is_hidden IS NULL)
        
        UNION ALL
        
        -- Recursively add children of visible nodes
        SELECT child.* FROM skill_tree_nodes child
        INNER JOIN visible_tree parent ON child.parent_id = parent.id
        WHERE child.is_hidden = FALSE OR child.is_hidden IS NULL
    )
    SELECT * FROM visible_tree;
END;
$$ LANGUAGE plpgsql STABLE;

-- Step 5: Grant permissions
GRANT EXECUTE ON FUNCTION get_visible_nodes() TO anon, authenticated;

-- Step 6: Create RLS policies if needed
-- Allow all authenticated users to read non-hidden nodes
CREATE POLICY "Users can view non-hidden nodes" ON skill_tree_nodes
    FOR SELECT
    TO authenticated
    USING (is_hidden = FALSE OR is_hidden IS NULL);

-- Allow admins to see all nodes (you'll need to adjust this based on your admin detection logic)
-- This example assumes you have an is_admin function or admin role
-- CREATE POLICY "Admins can view all nodes" ON skill_tree_nodes
--     FOR SELECT
--     TO authenticated
--     USING (auth.uid() IN (SELECT user_id FROM admin_users));

-- Step 7: Verify the column was added
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'skill_tree_nodes' AND column_name = 'is_hidden';