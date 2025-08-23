-- Drop only the old difficulty name columns from spelling_words table
-- These columns are no longer needed as we now use foreign keys with joined tables

-- Step 1: Create backup table (adjust name if _bkp3 already exists)
CREATE TABLE spelling_words_bkp3 AS 
SELECT * FROM spelling_words;

-- Verify backup
SELECT 
    (SELECT COUNT(*) FROM spelling_words) as original_count,
    (SELECT COUNT(*) FROM spelling_words_bkp3) as backup_count;

-- Step 2: Drop only the two name columns
ALTER TABLE spelling_words 
  DROP COLUMN IF EXISTS spelling_difficulty_name,
  DROP COLUMN IF EXISTS vocabulary_difficulty_name;

-- Step 3: Verify the columns were dropped
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'spelling_words' 
AND table_schema = 'public'
AND column_name IN ('spelling_difficulty_name', 'vocabulary_difficulty_name');
-- This should return 0 rows

-- Step 4: Verify foreign keys still work with joined names
SELECT 
    sw.word,
    sw.spelling_difficulty_id,
    sd.name as spelling_difficulty,
    sw.vocabulary_difficulty_id,
    vd.name as vocabulary_difficulty
FROM spelling_words sw
LEFT JOIN spelling_difficulty_levels sd ON sw.spelling_difficulty_id = sd.id
LEFT JOIN vocabulary_difficulty_levels vd ON sw.vocabulary_difficulty_id = vd.id
LIMIT 10;

-- Step 5: Count to ensure data integrity
SELECT 
    COUNT(*) as total_words,
    COUNT(spelling_difficulty_id) as has_spelling_difficulty,
    COUNT(vocabulary_difficulty_id) as has_vocabulary_difficulty
FROM spelling_words;