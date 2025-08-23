-- Find the correct skill_id for Money Counting
-- First, let's see what's in user_progress to understand the pattern

-- Check existing user_progress records with their linked data
SELECT 
    up.skill_id,
    up.status,
    up.rating,
    up.last_accessed
FROM user_progress up
WHERE up.user_id = auth.uid()
ORDER BY up.last_accessed DESC
LIMIT 10;

-- Check if there's a mapping between skill_tree_nodes and integer IDs
-- Perhaps through a different column or relationship
SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'skill_tree_nodes'
AND column_name LIKE '%id%' OR column_name LIKE '%skill%'
ORDER BY ordinal_position;

-- Look for Money Counting in skill_tree_nodes with all its fields
SELECT 
    *
FROM skill_tree_nodes
WHERE LOWER(name) LIKE '%money%counting%'
LIMIT 5;

-- Check if there's a skills or learning_modules table that maps to skill_tree_nodes
SELECT 
    t.table_name,
    t.table_type
FROM information_schema.tables t
WHERE t.table_schema = 'public'
AND (t.table_name LIKE '%skill%' OR t.table_name LIKE '%module%' OR t.table_name LIKE '%learning%')
ORDER BY t.table_name;