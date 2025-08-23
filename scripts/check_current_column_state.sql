-- Check current column state in all relevant tables
-- This script will show what columns currently exist

-- Check user_progress columns
SELECT 
    'user_progress' as table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
    AND table_name = 'user_progress'
    AND column_name IN ('skill_id', 'skill_node_id', 'node_id', 'skill_tree_node_id')
ORDER BY column_name;

-- Check starred_categories columns
SELECT 
    'starred_categories' as table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
    AND table_name = 'starred_categories'
    AND column_name IN ('skill_id', 'skill_node_id', 'node_id', 'skill_tree_node_id')
ORDER BY column_name;

-- Check questions columns
SELECT 
    'questions' as table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
    AND table_name = 'questions'
    AND column_name IN ('skill_id', 'skill_node_id', 'node_id', 'skill_tree_node_id')
ORDER BY column_name;

-- Check money_counting_progress columns
SELECT 
    'money_counting_progress' as table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
    AND table_name = 'money_counting_progress'
    AND column_name IN ('skill_id', 'skill_node_id', 'node_id', 'skill_tree_node_id')
ORDER BY column_name;

-- Check if backup tables exist
SELECT 
    table_name
FROM information_schema.tables
WHERE table_schema = 'public'
    AND (table_name LIKE 'user_progress_bkp%' 
         OR table_name LIKE 'starred_categories_bkp%')
ORDER BY table_name;