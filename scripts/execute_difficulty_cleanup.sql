-- SQL Script to Clean Up Old Difficulty Columns from spelling_words table
-- Generated: 2025-01-23
-- Purpose: Remove old text-based difficulty columns, keeping only foreign key references

-- ============================================================
-- STEP 1: CREATE BACKUP TABLE
-- ============================================================
-- This creates a complete backup of the spelling_words table before making changes
CREATE TABLE spelling_words_bkp_20250123 AS SELECT * FROM spelling_words;

-- Verify backup was created successfully
SELECT COUNT(*) as backup_count FROM spelling_words_bkp_20250123;

-- ============================================================
-- STEP 2: REMOVE OLD DIFFICULTY COLUMNS
-- ============================================================
-- These columns stored difficulty as text/numbers directly in the table
-- Now using foreign keys to difficulties table instead

-- Remove old spelling difficulty columns
ALTER TABLE spelling_words DROP COLUMN IF EXISTS spelling_difficulty_level;
ALTER TABLE spelling_words DROP COLUMN IF EXISTS spelling_difficulty_name;
ALTER TABLE spelling_words DROP COLUMN IF EXISTS ai_spelling_difficulty_level;
ALTER TABLE spelling_words DROP COLUMN IF EXISTS ai_spelling_difficulty_name;

-- Remove old vocabulary difficulty columns  
ALTER TABLE spelling_words DROP COLUMN IF EXISTS vocabulary_difficulty_level;
ALTER TABLE spelling_words DROP COLUMN IF EXISTS vocabulary_difficulty_name;

-- Remove unused/legacy difficulty columns
ALTER TABLE spelling_words DROP COLUMN IF EXISTS difficulty;
ALTER TABLE spelling_words DROP COLUMN IF EXISTS source_difficulty;

-- ============================================================
-- STEP 3: VERIFY REMAINING DIFFICULTY COLUMNS
-- ============================================================
-- Should only show spelling_difficulty_id and vocabulary_difficulty_id
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'spelling_words' 
    AND column_name LIKE '%difficulty%'
ORDER BY column_name;

-- ============================================================
-- STEP 4: VERIFY FOREIGN KEY CONSTRAINTS
-- ============================================================
-- Check that foreign key relationships are properly set up
SELECT
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.table_name = 'spelling_words'
    AND tc.constraint_type = 'FOREIGN KEY'
    AND kcu.column_name LIKE '%difficulty%';

-- ============================================================
-- STEP 5: VERIFY DATA INTEGRITY
-- ============================================================
-- Ensure all difficulty IDs reference valid difficulties
SELECT 
    COUNT(*) as total_words,
    COUNT(spelling_difficulty_id) as has_spelling_difficulty,
    COUNT(vocabulary_difficulty_id) as has_vocabulary_difficulty
FROM spelling_words;

-- Check for any orphaned difficulty IDs
SELECT DISTINCT s.spelling_difficulty_id
FROM spelling_words s
LEFT JOIN difficulties d ON s.spelling_difficulty_id = d.id
WHERE s.spelling_difficulty_id IS NOT NULL 
    AND d.id IS NULL;

SELECT DISTINCT s.vocabulary_difficulty_id
FROM spelling_words s
LEFT JOIN difficulties d ON s.vocabulary_difficulty_id = d.id
WHERE s.vocabulary_difficulty_id IS NOT NULL 
    AND d.id IS NULL;

-- ============================================================
-- CLEANUP COMPLETE
-- ============================================================
-- If all verifications pass, the old columns have been successfully removed
-- The backup table spelling_words_bkp_20250123 can be kept for safety
-- or dropped later with: DROP TABLE spelling_words_bkp_20250123;