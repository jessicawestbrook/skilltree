-- Pre-migration check script to see what columns exist in each table
-- Run this BEFORE the migration to understand your current schema

-- Check skill_tree_nodes columns
SELECT 
    'skill_tree_nodes' as table_name,
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public'
    AND table_name = 'skill_tree_nodes'
ORDER BY 
    ordinal_position;

-- Check questions columns
SELECT 
    'questions' as table_name,
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public'
    AND table_name = 'questions'
ORDER BY 
    ordinal_position;

-- Check user_progress columns
SELECT 
    'user_progress' as table_name,
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public'
    AND table_name = 'user_progress'
ORDER BY 
    ordinal_position;

-- Check starred_items columns
SELECT 
    'starred_items' as table_name,
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public'
    AND table_name = 'starred_items'
ORDER BY 
    ordinal_position;

-- Check learning_content columns
SELECT 
    'learning_content' as table_name,
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public'
    AND table_name = 'learning_content'
ORDER BY 
    ordinal_position;

-- Check skill_learning_content columns (if exists)
SELECT 
    'skill_learning_content' as table_name,
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public'
    AND table_name = 'skill_learning_content'
ORDER BY 
    ordinal_position;

-- Find ALL columns that might reference skill_tree_nodes
SELECT DISTINCT
    c.table_name,
    c.column_name,
    c.data_type,
    CASE 
        WHEN kcu.column_name IS NOT NULL THEN 'Has FK constraint to: ' || ccu.table_name || '(' || ccu.column_name || ')'
        ELSE 'No FK constraint'
    END as constraint_info
FROM 
    information_schema.columns c
    LEFT JOIN information_schema.key_column_usage kcu 
        ON c.table_name = kcu.table_name 
        AND c.column_name = kcu.column_name
        AND c.table_schema = kcu.table_schema
    LEFT JOIN information_schema.constraint_column_usage ccu
        ON kcu.constraint_name = ccu.constraint_name
        AND kcu.table_schema = ccu.table_schema
WHERE 
    c.table_schema = 'public'
    AND (
        c.column_name LIKE '%skill%' 
        OR c.column_name LIKE '%node%'
        OR c.column_name = 'parent_id'
        OR c.column_name = 'category_id'
        OR c.column_name = 'test_id'
        OR c.column_name = 'item_id'
    )
    AND c.data_type IN ('text', 'character varying')
ORDER BY 
    c.table_name, c.column_name;