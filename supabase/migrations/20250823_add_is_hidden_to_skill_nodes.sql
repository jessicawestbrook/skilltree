-- Add is_hidden field to skill_tree_nodes table to control visibility
ALTER TABLE skill_tree_nodes 
ADD COLUMN IF NOT EXISTS is_hidden BOOLEAN DEFAULT FALSE;

-- Create index for performance when filtering
CREATE INDEX IF NOT EXISTS idx_skill_tree_nodes_is_hidden 
ON skill_tree_nodes(is_hidden);

-- Add comment for documentation
COMMENT ON COLUMN skill_tree_nodes.is_hidden IS 'When true, hides this node and all its descendants from non-admin users';

-- Create a function to check if a node should be visible (considering parent visibility)
CREATE OR REPLACE FUNCTION is_node_visible(node_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    current_id UUID := node_id;
    parent_id UUID;
    is_hidden BOOLEAN;
BEGIN
    -- Check each node in the hierarchy up to the root
    WHILE current_id IS NOT NULL LOOP
        SELECT stn.parent_id, stn.is_hidden 
        INTO parent_id, is_hidden
        FROM skill_tree_nodes stn
        WHERE stn.id = current_id;
        
        -- If any parent (including self) is hidden, node is not visible
        IF is_hidden = TRUE THEN
            RETURN FALSE;
        END IF;
        
        current_id := parent_id;
    END LOOP;
    
    -- If we made it through all parents without finding a hidden one, node is visible
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql STABLE;

-- Create a view for visible nodes (useful for queries)
CREATE OR REPLACE VIEW visible_skill_tree_nodes AS
SELECT stn.*
FROM skill_tree_nodes stn
WHERE is_node_visible(stn.id);

-- Grant appropriate permissions
GRANT SELECT ON visible_skill_tree_nodes TO anon, authenticated;