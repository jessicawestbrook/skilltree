-- Script to drop duplicate response tables after verification
-- Run this in Supabase SQL Editor

-- First, verify all tables are empty
SELECT 'question_responses' as table_name, COUNT(*) as row_count FROM question_responses
UNION ALL
SELECT 'assessment_question_responses', COUNT(*) FROM assessment_question_responses
UNION ALL
SELECT 'user_test_responses', COUNT(*) FROM user_test_responses
UNION ALL
SELECT 'user_question_attempts', COUNT(*) FROM user_question_attempts;

-- Verify the unified table exists
SELECT COUNT(*) as unified_table_row_count FROM user_question_responses;

-- If all duplicate tables show 0 rows, proceed with dropping them:
-- IMPORTANT: Only uncomment and run the DROP statements after confirming all tables are empty

-- DROP TABLE IF EXISTS question_responses CASCADE;
-- DROP TABLE IF EXISTS assessment_question_responses CASCADE;
-- DROP TABLE IF EXISTS user_test_responses CASCADE;
-- DROP TABLE IF EXISTS user_question_attempts CASCADE;

-- After dropping, verify they no longer exist:
-- SELECT table_name FROM information_schema.tables 
-- WHERE table_schema = 'public' 
-- AND table_name IN ('question_responses', 'assessment_question_responses', 'user_test_responses', 'user_question_attempts');