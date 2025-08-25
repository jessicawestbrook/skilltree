-- Delete Vector Calculus node that is directly under Calculus
-- This node should be removed as Vector Calculus topics are now under Multivariable Calculus

-- First verify this is the correct node
SELECT id, name, parent_id 
FROM skill_tree_nodes 
WHERE id = '3fad74c8-6f01-4294-9f92-01d58b54b633';

-- Check for any children (should be none based on our check)
SELECT COUNT(*) as child_count 
FROM skill_tree_nodes 
WHERE parent_id = '3fad74c8-6f01-4294-9f92-01d58b54b633';

-- Delete the Vector Calculus node
DELETE FROM skill_tree_nodes 
WHERE id = '3fad74c8-6f01-4294-9f92-01d58b54b633';

-- Verify deletion
SELECT id, name 
FROM skill_tree_nodes 
WHERE id = '3fad74c8-6f01-4294-9f92-01d58b54b633';

-- Show remaining Calculus children (should only show 4: Differential Calculus, Integral Calculus, Multivariable Calculus, Differential Equations)
SELECT name 
FROM skill_tree_nodes 
WHERE parent_id = '9d533c45-708f-4485-a8d8-e8343bff0196'
ORDER BY name;