-- Check the structure of user_progress table
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'user_progress'
ORDER BY ordinal_position;

-- Check a sample of existing data
SELECT * FROM user_progress LIMIT 1;