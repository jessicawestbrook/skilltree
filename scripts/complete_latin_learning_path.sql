-- Complete Henle Latin Learning Path Setup
-- This creates all necessary tables and inserts the complete Henle Latin curriculum

-- First, create the learning paths tables if they don't exist
-- (Run create_learning_paths_tables.sql separately if needed)

-- Then run the course creation
-- (This is in create_complete_henle_latin_path.sql)

-- For now, let's create a preview of what will be inserted
SELECT 'This script will create:' as info
UNION ALL
SELECT '- Learning paths table structure'
UNION ALL  
SELECT '- 4 additional Henle Latin courses (Second Year, Third Year, Fourth Year, Grammar)'
UNION ALL
SELECT '- Complete Henle Latin Learning Path linking all 5 courses'
UNION ALL
SELECT '- Total estimated time: 420 hours across all courses';

-- To execute:
-- 1. Run create_learning_paths_tables.sql
-- 2. Run create_complete_henle_latin_path.sql