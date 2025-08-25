-- Remove AI-generated spelling difficulty fields from spelling_words table
-- This removes ai_spelling_difficulty_level and ai_spelling_difficulty_name

-- ============================================================================
-- STEP 1: CREATE BACKUP BEFORE REMOVING FIELDS
-- ============================================================================

-- Create backup with timestamp
CREATE TABLE IF NOT EXISTS spelling_words_bkp_before_ai_removal AS 
SELECT * FROM spelling_words;

-- Verify backup was created
SELECT 
    'Backup Created' as status,
    COUNT(*) as rows_backed_up 
FROM spelling_words_bkp_before_ai_removal;

-- ============================================================================
-- STEP 2: CHECK CURRENT VALUES IN AI FIELDS (for documentation)
-- ============================================================================

-- Show distribution of AI difficulty levels before removal
SELECT 
    'AI Spelling Difficulty Level Distribution (before removal)' as info;

SELECT 
    ai_spelling_difficulty_level,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM spelling_words), 0), 2) as percentage
FROM spelling_words
GROUP BY ai_spelling_difficulty_level
ORDER BY ai_spelling_difficulty_level;

-- Show sample of AI difficulty names
SELECT 
    'AI Spelling Difficulty Names (before removal)' as info;

SELECT DISTINCT 
    ai_spelling_difficulty_name,
    COUNT(*) as count
FROM spelling_words
WHERE ai_spelling_difficulty_name IS NOT NULL
GROUP BY ai_spelling_difficulty_name
ORDER BY ai_spelling_difficulty_name
LIMIT 10;

-- ============================================================================
-- STEP 3: DROP THE AI FIELDS
-- ============================================================================

-- Drop ai_spelling_difficulty_level column
ALTER TABLE spelling_words 
DROP COLUMN IF EXISTS ai_spelling_difficulty_level;

-- Drop ai_spelling_difficulty_name column
ALTER TABLE spelling_words 
DROP COLUMN IF EXISTS ai_spelling_difficulty_name;

-- ============================================================================
-- STEP 4: VERIFY REMOVAL
-- ============================================================================

-- List remaining difficulty-related columns
SELECT 
    'Remaining difficulty columns after AI field removal:' as info,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'spelling_words'
AND column_name LIKE '%difficulty%'
ORDER BY ordinal_position;

-- ============================================================================
-- STEP 5: FINAL SUMMARY
-- ============================================================================

SELECT 
    'Summary - Difficulty Fields Still in Table:' as info;

SELECT 
    'spelling_difficulty_level' as field_name,
    'INTEGER (1-5)' as type,
    'XGBoost predictions' as source,
    COUNT(spelling_difficulty_level) as populated_count
FROM spelling_words
UNION ALL
SELECT 
    'vocabulary_difficulty_level' as field_name,
    'INTEGER (1-5)' as type,
    'Frequency-based bins' as source,
    COUNT(vocabulary_difficulty_level) as populated_count
FROM spelling_words
UNION ALL
SELECT 
    'source_difficulty' as field_name,
    'VARCHAR' as type,
    'Original bee ratings' as source,
    COUNT(source_difficulty) as populated_count
FROM spelling_words;

-- ============================================================================
-- NOTES:
-- - The ai_spelling_difficulty_level and ai_spelling_difficulty_name fields have been removed
-- - The main spelling_difficulty_level (XGBoost) remains
-- - The vocabulary_difficulty_level (frequency-based) remains
-- - The source_difficulty (bee ratings) remains as the gold standard
-- - Backup table spelling_words_bkp_before_ai_removal contains the original data
-- ============================================================================