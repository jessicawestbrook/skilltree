-- Remove AI-generated spelling difficulty fields and handle view dependencies
-- This script drops and recreates views without the AI fields

-- ============================================================================
-- STEP 1: CREATE BACKUP
-- ============================================================================

CREATE TABLE IF NOT EXISTS spelling_words_bkp_before_ai_removal AS 
SELECT * FROM spelling_words;

-- ============================================================================
-- STEP 2: DROP DEPENDENT VIEWS
-- ============================================================================

-- Drop views that depend on the AI columns
DROP VIEW IF EXISTS spelling_words_with_sources CASCADE;
DROP VIEW IF EXISTS spelling_words_with_difficulty_names CASCADE;

-- ============================================================================
-- STEP 3: DROP THE AI COLUMNS
-- ============================================================================

-- Now we can safely drop the AI columns
ALTER TABLE spelling_words 
DROP COLUMN IF EXISTS ai_spelling_difficulty_level CASCADE;

ALTER TABLE spelling_words 
DROP COLUMN IF EXISTS ai_spelling_difficulty_name CASCADE;

-- ============================================================================
-- STEP 4: RECREATE VIEWS WITHOUT AI FIELDS
-- ============================================================================

-- Recreate spelling_words_with_sources view without AI fields
CREATE OR REPLACE VIEW spelling_words_with_sources AS
SELECT 
    sw.id,
    sw.word,
    sw.definition,
    sw.example_sentence,
    sw.source_difficulty,
    sw.spelling_difficulty_level,
    sw.vocabulary_difficulty_level,
    sw.frequency,
    sw.phonetic_transparency_score,
    sw.word_frequency_score,
    sw.morphology_score,
    sw.etymology_score,
    sw.spelling_difficulty_calculation_method,
    sw.part_of_speech,
    sw.pronunciation_guide,
    sw.etymology,
    sw.etymology_source,
    sw.memory_tips,
    sw.alternate_spellings,
    sw.language_origin,
    sw.definition_source,
    sw.source_names,
    sw.original_source,
    sw.source_access_date,
    sw.created_at,
    sw.updated_at,
    sw.vocabulary_semantic_complexity_score,
    sw.vocabulary_contextual_frequency_score,
    sw.vocabulary_conceptual_sophistication_score,
    sw.vocabulary_register_specificity_score,
    sw.vocabulary_difficulty_calculation_method,
    sw.spelling_difficulty_id,
    sw.vocabulary_difficulty_id,
    sw.grade_level,
    sw.is_spelling_word,
    sw.is_vocabulary_word
FROM spelling_words sw;

-- Recreate spelling_words_with_difficulty_names view without AI fields
CREATE OR REPLACE VIEW spelling_words_with_difficulty_names AS
SELECT 
    sw.*,
    -- Spelling difficulty name based on level
    CASE sw.spelling_difficulty_level
        WHEN 1 THEN 'Very Easy'
        WHEN 2 THEN 'Easy'
        WHEN 3 THEN 'Medium'
        WHEN 4 THEN 'Hard'
        WHEN 5 THEN 'Very Hard'
        ELSE 'Unknown'
    END AS spelling_difficulty_name,
    -- Vocabulary difficulty name based on level
    CASE sw.vocabulary_difficulty_level
        WHEN 1 THEN 'Basic'
        WHEN 2 THEN 'Elementary'
        WHEN 3 THEN 'Intermediate'
        WHEN 4 THEN 'Advanced'
        WHEN 5 THEN 'Expert'
        ELSE 'Unknown'
    END AS vocabulary_difficulty_name,
    -- Frequency category for additional context
    CASE 
        WHEN sw.frequency >= 6 THEN 'Very Common'
        WHEN sw.frequency >= 5 THEN 'Common'
        WHEN sw.frequency >= 4 THEN 'Moderate'
        WHEN sw.frequency >= 3 THEN 'Uncommon'
        WHEN sw.frequency >= 2 THEN 'Rare'
        WHEN sw.frequency >= 0 THEN 'Very Rare'
        ELSE 'Unknown'
    END AS frequency_category
FROM spelling_words sw;

-- ============================================================================
-- STEP 5: VERIFY REMOVAL AND VIEW RECREATION
-- ============================================================================

-- Check that AI columns are gone
SELECT 
    'Columns with "ai" in name (should be empty):' as check,
    COUNT(*) as ai_columns_remaining
FROM information_schema.columns
WHERE table_name = 'spelling_words'
AND column_name LIKE '%ai%';

-- Verify views exist and work
SELECT 
    'Views recreated successfully:' as status;

-- Test the views
SELECT COUNT(*) as rows_in_sources_view 
FROM spelling_words_with_sources
LIMIT 1;

SELECT COUNT(*) as rows_in_difficulty_names_view 
FROM spelling_words_with_difficulty_names
LIMIT 1;

-- Show remaining difficulty columns
SELECT 
    'Remaining difficulty columns:' as info,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'spelling_words'
AND column_name LIKE '%difficulty%'
ORDER BY ordinal_position;

-- ============================================================================
-- STEP 6: SUMMARY
-- ============================================================================

SELECT 'REMOVAL COMPLETE' as status;

SELECT 
    'Summary of remaining difficulty fields:' as info;

SELECT 
    'spelling_difficulty_level' as field,
    COUNT(*) as populated,
    ROUND(AVG(spelling_difficulty_level)::numeric, 2) as average
FROM spelling_words
WHERE spelling_difficulty_level IS NOT NULL
UNION ALL
SELECT 
    'vocabulary_difficulty_level' as field,
    COUNT(*) as populated,
    ROUND(AVG(vocabulary_difficulty_level)::numeric, 2) as average
FROM spelling_words
WHERE vocabulary_difficulty_level IS NOT NULL
UNION ALL
SELECT 
    'frequency' as field,
    COUNT(*) as populated,
    ROUND(AVG(frequency)::numeric, 2) as average
FROM spelling_words
WHERE frequency IS NOT NULL;

-- Sample from the recreated view with difficulty names
SELECT 
    'Sample from difficulty names view:' as info;

SELECT 
    word,
    spelling_difficulty_level,
    spelling_difficulty_name,
    vocabulary_difficulty_level,
    vocabulary_difficulty_name,
    ROUND(frequency::numeric, 2) as freq,
    frequency_category
FROM spelling_words_with_difficulty_names
WHERE spelling_difficulty_level IS NOT NULL
AND vocabulary_difficulty_level IS NOT NULL
ORDER BY RANDOM()
LIMIT 5;