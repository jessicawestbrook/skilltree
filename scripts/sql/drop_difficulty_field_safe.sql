-- Safe script to drop the empty difficulty field from spelling_words table
-- This handles the dependent view properly
-- Date: 2025-08-24
-- Purpose: Remove unused difficulty field that is 100% NULL

-- Step 1: Create backup table with timestamp
CREATE TABLE IF NOT EXISTS spelling_words_bkp_2025_08_24_drop_difficulty AS 
SELECT * FROM spelling_words;

-- Step 2: Add comment to backup table for documentation
COMMENT ON TABLE spelling_words_bkp_2025_08_24_drop_difficulty IS 
'Backup created before dropping empty difficulty field on 2025-08-24. Original table had 9901 rows with difficulty field 100% NULL.';

-- Step 3: Store the view definition before dropping it
-- The view includes the difficulty field, so we need to recreate it without that field
CREATE OR REPLACE VIEW spelling_words_with_sources_temp AS
SELECT 
    sw.id,
    sw.word,
    sw.definition,
    sw.part_of_speech,
    sw.example_sentence,
    sw.etymology,
    sw.pronunciation,
    sw.created_at,
    sw.updated_at,
    sw.source_difficulty,
    sw.spelling_difficulty_level,
    sw.ai_spelling_difficulty_level,
    sw.ai_spelling_difficulty_name,
    sw.spelling_difficulty_calculation_method,
    sw.vocabulary_difficulty_level,
    sw.vocabulary_difficulty_calculation_method,
    sw.spelling_difficulty_id,
    sw.vocabulary_difficulty_id,
    sw.grade_level,
    sw.frequency_score,
    sw.semantic_score,
    sw.morphological_score,
    sw.etymology_score,
    sw.overall_score,
    sw.is_compound,
    sw.morphological_features,
    sw.semantic_field,
    sw.register_formality,
    sw.additional_notes,
    sd.name as spelling_difficulty_name,
    vd.name as vocabulary_difficulty_name
FROM spelling_words sw
LEFT JOIN spelling_difficulty sd ON sw.spelling_difficulty_id = sd.id
LEFT JOIN vocabulary_difficulty vd ON sw.vocabulary_difficulty_id = vd.id;

-- Step 4: Drop the old view that depends on the difficulty column
DROP VIEW IF EXISTS spelling_words_with_sources CASCADE;

-- Step 5: Drop the difficulty column from spelling_words
ALTER TABLE spelling_words 
DROP COLUMN IF EXISTS difficulty;

-- Step 6: Recreate the view without the difficulty field
CREATE OR REPLACE VIEW spelling_words_with_sources AS
SELECT 
    sw.id,
    sw.word,
    sw.definition,
    sw.part_of_speech,
    sw.example_sentence,
    sw.etymology,
    sw.pronunciation,
    sw.created_at,
    sw.updated_at,
    sw.source_difficulty,
    sw.spelling_difficulty_level,
    sw.ai_spelling_difficulty_level,
    sw.ai_spelling_difficulty_name,
    sw.spelling_difficulty_calculation_method,
    sw.vocabulary_difficulty_level,
    sw.vocabulary_difficulty_calculation_method,
    sw.spelling_difficulty_id,
    sw.vocabulary_difficulty_id,
    sw.grade_level,
    sw.frequency_score,
    sw.semantic_score,
    sw.morphological_score,
    sw.etymology_score,
    sw.overall_score,
    sw.is_compound,
    sw.morphological_features,
    sw.semantic_field,
    sw.register_formality,
    sw.additional_notes,
    sd.name as spelling_difficulty_name,
    vd.name as vocabulary_difficulty_name
FROM spelling_words sw
LEFT JOIN spelling_difficulty sd ON sw.spelling_difficulty_id = sd.id
LEFT JOIN vocabulary_difficulty vd ON sw.vocabulary_difficulty_id = vd.id;

-- Step 7: Drop the temporary view
DROP VIEW IF EXISTS spelling_words_with_sources_temp;

-- Step 8: Grant appropriate permissions on the recreated view
GRANT SELECT ON spelling_words_with_sources TO anon, authenticated;

-- Step 9: Verify the changes
-- This query will show all difficulty-related fields that remain
SELECT column_name, data_type
FROM information_schema.columns 
WHERE table_name = 'spelling_words' 
AND column_name LIKE '%difficulty%'
ORDER BY column_name;

-- Expected remaining difficulty fields:
-- - ai_spelling_difficulty_level
-- - ai_spelling_difficulty_name
-- - source_difficulty
-- - spelling_difficulty_calculation_method
-- - spelling_difficulty_id
-- - spelling_difficulty_level
-- - vocabulary_difficulty_calculation_method
-- - vocabulary_difficulty_id
-- - vocabulary_difficulty_level

-- The 'difficulty' field should no longer appear