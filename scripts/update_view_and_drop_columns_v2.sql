-- Update view and drop old difficulty name columns and source_difficulties from spelling_words table

-- Step 1: Drop and recreate the view without the columns being dropped
DROP VIEW IF EXISTS spelling_words_with_sources CASCADE;

CREATE VIEW spelling_words_with_sources AS
SELECT 
    sw.id,
    sw.word,
    sw.definition,
    sw.example_sentence,
    sw.part_of_speech,
    sw.pronunciation_guide,
    sw.etymology,
    sw.etymology_source,
    sw.memory_tips,
    sw.alternate_spellings,
    sw.language_origin,
    sw.definition_source,
    sw.source_names,
    -- source_difficulties will be removed
    sw.frequency,
    sw.original_source,
    sw.source_access_date,
    sw.created_at,
    sw.updated_at,
    sw.spelling_difficulty_id,
    sw.vocabulary_difficulty_id,
    -- Join to get difficulty names from the foreign key tables
    sd.name as spelling_difficulty_name,
    vd.name as vocabulary_difficulty_name,
    -- Keep other columns that aren't being dropped
    sw.source_difficulty,
    sw.spelling_difficulty_level,
    sw.ai_spelling_difficulty_level,
    sw.ai_spelling_difficulty_name,
    sw.phonetic_transparency_score,
    sw.word_frequency_score,
    sw.morphology_score,
    sw.etymology_score,
    sw.spelling_difficulty_calculation_method,
    sw.vocabulary_difficulty_level,
    sw.vocabulary_semantic_complexity_score,
    sw.vocabulary_contextual_frequency_score,
    sw.vocabulary_conceptual_sophistication_score,
    sw.vocabulary_register_specificity_score,
    sw.vocabulary_difficulty_calculation_method,
    sw.grade_level,
    sw.difficulty
FROM spelling_words sw
LEFT JOIN spelling_difficulty_levels sd ON sw.spelling_difficulty_id = sd.id
LEFT JOIN vocabulary_difficulty_levels vd ON sw.vocabulary_difficulty_id = vd.id;

-- Step 2: Create backup table (adjust name if _bkp3 already exists)
CREATE TABLE IF NOT EXISTS spelling_words_bkp3 AS 
SELECT * FROM spelling_words;

-- Verify backup
SELECT 
    (SELECT COUNT(*) FROM spelling_words) as original_count,
    (SELECT COUNT(*) FROM spelling_words_bkp3) as backup_count;

-- Step 3: Now we can safely drop the columns
ALTER TABLE spelling_words 
  DROP COLUMN IF EXISTS spelling_difficulty_name,
  DROP COLUMN IF EXISTS vocabulary_difficulty_name,
  DROP COLUMN IF EXISTS source_difficulties;

-- Step 4: Verify the columns were dropped
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'spelling_words' 
AND table_schema = 'public'
AND column_name IN ('spelling_difficulty_name', 'vocabulary_difficulty_name', 'source_difficulties');
-- This should return 0 rows

-- Step 5: Test the updated view
SELECT 
    word,
    spelling_difficulty_name,
    vocabulary_difficulty_name
FROM spelling_words_with_sources
LIMIT 5;

-- Step 6: Verify foreign keys still work
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

-- Step 7: Count to ensure data integrity
SELECT 
    COUNT(*) as total_words,
    COUNT(spelling_difficulty_id) as has_spelling_difficulty,
    COUNT(vocabulary_difficulty_id) as has_vocabulary_difficulty
FROM spelling_words;

-- Step 8: Show remaining columns in spelling_words table
SELECT column_name, data_type
FROM information_schema.columns 
WHERE table_name = 'spelling_words' 
AND table_schema = 'public'
ORDER BY ordinal_position;