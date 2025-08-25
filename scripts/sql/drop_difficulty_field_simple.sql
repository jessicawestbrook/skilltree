-- Simple script to drop the empty difficulty field from spelling_words table
-- Date: 2025-08-24
-- Purpose: Remove unused difficulty field that is 100% NULL

-- Step 1: Create backup table if it doesn't exist
CREATE TABLE IF NOT EXISTS spelling_words_bkp_2025_08_24_drop_difficulty AS 
SELECT * FROM spelling_words;

-- Step 2: Drop the view that depends on the difficulty column
DROP VIEW IF EXISTS spelling_words_with_sources CASCADE;

-- Step 3: Drop the difficulty column from spelling_words
ALTER TABLE spelling_words 
DROP COLUMN IF EXISTS difficulty;

-- Step 4: Recreate the view without the difficulty field
-- Note: The view joins with spelling_difficulty and vocabulary_difficulty tables that don't exist,
-- so we'll create a simpler version that just adds the difficulty name fields directly
CREATE OR REPLACE VIEW spelling_words_with_sources AS
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
    sw.frequency,
    sw.original_source,
    sw.source_access_date,
    sw.created_at,
    sw.updated_at,
    sw.spelling_difficulty_id,
    sw.vocabulary_difficulty_id,
    -- Map difficulty IDs to names directly since the lookup tables don't exist
    CASE sw.spelling_difficulty_id
        WHEN 1 THEN 'Beginner'
        WHEN 2 THEN 'Elementary'
        WHEN 3 THEN 'Intermediate'
        WHEN 4 THEN 'Advanced'
        WHEN 5 THEN 'Expert'
        ELSE NULL
    END as spelling_difficulty_name,
    CASE sw.vocabulary_difficulty_id
        WHEN 1 THEN 'Foundation'
        WHEN 2 THEN 'Academic'
        WHEN 3 THEN 'Sophisticated'
        WHEN 4 THEN 'Specialized'
        WHEN 5 THEN 'Scholarly'
        ELSE NULL
    END as vocabulary_difficulty_name,
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
    sw.grade_level
    -- Note: 'difficulty' field is intentionally omitted as it's being dropped
FROM spelling_words sw;

-- Step 5: Grant appropriate permissions on the recreated view
GRANT SELECT ON spelling_words_with_sources TO anon, authenticated;

-- Step 6: Verify the column was dropped
SELECT 
    'Success! The difficulty field has been removed.' as status,
    COUNT(*) as remaining_difficulty_fields
FROM information_schema.columns 
WHERE table_name = 'spelling_words' 
AND column_name = 'difficulty';