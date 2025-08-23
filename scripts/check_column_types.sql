-- Check the data types of all relevant columns
SELECT 
    table_name,
    column_name,
    data_type,
    udt_name,
    character_maximum_length,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
    AND table_name IN ('user_progress', 'starred_categories', 'skill_tree_nodes')
    AND (column_name LIKE '%skill%' OR column_name = 'id' OR column_name LIKE '%node%')
ORDER BY table_name, column_name;

-- Specifically check skill_tree_nodes.id type
SELECT 
    'skill_tree_nodes.id' as field,
    data_type,
    udt_name
FROM information_schema.columns
WHERE table_schema = 'public'
    AND table_name = 'skill_tree_nodes'
    AND column_name = 'id';

-- Check user_progress columns
SELECT 
    'user_progress columns' as table_info,
    column_name,
    data_type,
    udt_name
FROM information_schema.columns
WHERE table_schema = 'public'
    AND table_name = 'user_progress'
ORDER BY ordinal_position;