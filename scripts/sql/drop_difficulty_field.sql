-- Script to drop the empty difficulty field from spelling_words table
-- Date: 2025-08-24
-- Purpose: Remove unused difficulty field that is 100% NULL

-- Step 1: Create backup table with timestamp
CREATE TABLE spelling_words_bkp_2025_08_24_drop_difficulty AS 
SELECT * FROM spelling_words;

-- Step 2: Add comment to backup table for documentation
COMMENT ON TABLE spelling_words_bkp_2025_08_24_drop_difficulty IS 
'Backup created before dropping empty difficulty field on 2025-08-24. Original table had 9901 rows with difficulty field 100% NULL.';

-- Step 3: Verify backup was created successfully (manual check)
-- Run this to confirm row count matches:
-- SELECT COUNT(*) FROM spelling_words_bkp_2025_08_24_drop_difficulty;
-- Should return 9901 rows

-- Step 4: Drop the difficulty column from spelling_words
ALTER TABLE spelling_words 
DROP COLUMN IF EXISTS difficulty;

-- Step 5: Verify the column was dropped (manual check)
-- Run this to see remaining columns:
-- SELECT column_name 
-- FROM information_schema.columns 
-- WHERE table_name = 'spelling_words' 
-- AND column_name LIKE '%difficulty%'
-- ORDER BY column_name;

-- Should show these difficulty-related fields remain:
-- - source_difficulty (the gold standard bee ratings)
-- - spelling_difficulty_level
-- - ai_spelling_difficulty_level  
-- - ai_spelling_difficulty_name
-- - spelling_difficulty_calculation_method
-- - vocabulary_difficulty_level
-- - vocabulary_difficulty_calculation_method
-- - spelling_difficulty_id
-- - vocabulary_difficulty_id

-- The 'difficulty' field should no longer appear