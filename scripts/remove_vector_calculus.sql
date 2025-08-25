-- Script to remove Vector Calculus node directly under Calculus
-- Vector Calculus ID: 3fad74c8-6f01-4294-9f92-01d58b54b633

-- First, create a backup of the skill_tree_nodes table
CREATE TABLE IF NOT EXISTS skill_tree_nodes_bkp AS 
SELECT * FROM skill_tree_nodes;

-- Check if any nodes have Vector Calculus as parent (children that would be orphaned)
SELECT COUNT(*) as child_count, STRING_AGG(name, ', ') as child_names
FROM skill_tree_nodes 
WHERE parent_id = '3fad74c8-6f01-4294-9f92-01d58b54b633';

-- Delete Vector Calculus and all its descendants recursively
WITH RECURSIVE descendants AS (
    -- Start with Vector Calculus node
    SELECT id FROM skill_tree_nodes 
    WHERE id = '3fad74c8-6f01-4294-9f92-01d58b54b633'
    
    UNION ALL
    
    -- Recursively find all descendants
    SELECT s.id 
    FROM skill_tree_nodes s
    INNER JOIN descendants d ON s.parent_id = d.id
)
DELETE FROM skill_tree_nodes 
WHERE id IN (SELECT id FROM descendants);

-- Verify deletion
SELECT COUNT(*) as remaining_count 
FROM skill_tree_nodes 
WHERE id = '3fad74c8-6f01-4294-9f92-01d58b54b633' 
   OR parent_id = '3fad74c8-6f01-4294-9f92-01d58b54b633';

-- Check remaining Calculus children
SELECT name 
FROM skill_tree_nodes 
WHERE parent_id = '9d533c45-708f-4485-a8d8-e8343bff0196'
ORDER BY name;