-- Check what columns exist in questions and learning_content tables
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public'
    AND table_name IN ('questions', 'learning_content', 'skill_learning_content')
ORDER BY 
    table_name, ordinal_position;