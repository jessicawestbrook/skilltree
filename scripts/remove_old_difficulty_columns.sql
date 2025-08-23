-- Remove old difficulty columns from spelling_words table
-- These columns are no longer needed as we now use foreign keys

-- Step 1: Create backup table (adjust name if _bkp2 already exists)
CREATE TABLE spelling_words_bkp2 AS 
SELECT * FROM spelling_words;

-- Verify backup
SELECT 
    (SELECT COUNT(*) FROM spelling_words) as original_count,
    (SELECT COUNT(*) FROM spelling_words_bkp2) as backup_count;

-- Step 2: Remove old difficulty columns
ALTER TABLE spelling_words 
  DROP COLUMN IF EXISTS source_difficulty,
  DROP COLUMN IF EXISTS spelling_difficulty_level,
  DROP COLUMN IF EXISTS spelling_difficulty_name,
  DROP COLUMN IF EXISTS ai_spelling_difficulty_level,
  DROP COLUMN IF EXISTS ai_spelling_difficulty_name,
  DROP COLUMN IF EXISTS spelling_difficulty_calculation_method,
  DROP COLUMN IF EXISTS vocabulary_difficulty_level,
  DROP COLUMN IF EXISTS vocabulary_difficulty_name,
  DROP COLUMN IF EXISTS vocabulary_difficulty_calculation_method,
  DROP COLUMN IF EXISTS vocabulary_semantic_complexity_score,
  DROP COLUMN IF EXISTS vocabulary_contextual_frequency_score,
  DROP COLUMN IF EXISTS vocabulary_conceptual_sophistication_score,
  DROP COLUMN IF EXISTS vocabulary_register_specificity_score,
  DROP COLUMN IF EXISTS grade_level,
  DROP COLUMN IF EXISTS difficulty;

-- Step 3: Verify remaining columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'spelling_words' 
AND table_schema = 'public'
ORDER BY ordinal_position;

-- Step 4: Verify foreign keys still work
SELECT 
    sw.word,
    sw.spelling_difficulty_id,
    sd.name as spelling_difficulty,
    sw.vocabulary_difficulty_id,
    vd.name as vocabulary_difficulty
FROM spelling_words sw
LEFT JOIN spelling_difficulty_levels sd ON sw.spelling_difficulty_id = sd.id
LEFT JOIN vocabulary_difficulty_levels vd ON sw.vocabulary_difficulty_id = vd.id
LIMIT 5;