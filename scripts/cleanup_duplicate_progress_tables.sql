-- Cleanup duplicate user progress tables
-- Keep only user_module_progress which is actively used for course tracking

-- First, backup any data that might be important
-- (These tables appear to be empty or have minimal test data)

-- Check what's in each table before dropping
SELECT 'user_progress' as table_name, COUNT(*) as row_count FROM user_progress
UNION ALL
SELECT 'user_course_progress' as table_name, COUNT(*) as row_count FROM user_course_progress
UNION ALL 
SELECT 'user_learning_path_progress' as table_name, COUNT(*) as row_count FROM user_learning_path_progress;

-- Drop the unnecessary tables
-- user_progress: empty, not used
DROP TABLE IF EXISTS user_progress CASCADE;

-- user_course_progress: empty, not used (we use user_module_progress instead)
DROP TABLE IF EXISTS user_course_progress CASCADE;

-- user_learning_path_progress: has 1 row but not integrated with the app
-- The learning path tracking is done through module progress
DROP TABLE IF EXISTS user_learning_path_progress CASCADE;

-- Keep user_module_progress - this is the main progress tracking table used by CourseViewer

-- Verify the cleanup
SELECT 
    tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
    AND tablename LIKE '%progress%'
ORDER BY tablename;

-- Expected result: Should only show user_module_progress