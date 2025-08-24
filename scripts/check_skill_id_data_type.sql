-- Check the current data type of skill_id columns in various tables
SELECT 
    table_name,
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
    AND column_name = 'skill_id'
ORDER BY table_name;

-- Check if there are any foreign key constraints
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    tc.constraint_name
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND kcu.column_name = 'skill_id'
    AND tc.table_schema = 'public';

-- Check sample data from user_progress to see current skill_id values
SELECT 
    skill_id,
    pg_typeof(skill_id) as data_type,
    user_id,
    last_accessed
FROM user_progress
LIMIT 5;

-- Check if skill_id values are valid UUIDs
SELECT 
    COUNT(*) as total_rows,
    COUNT(CASE WHEN skill_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN 1 END) as valid_uuid_format,
    COUNT(CASE WHEN skill_id IS NULL THEN 1 END) as null_values
FROM user_progress;