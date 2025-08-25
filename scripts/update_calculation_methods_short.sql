-- Update the calculation method fields with shorter descriptions (50 char limit)

-- ============================================================================
-- STEP 1: UPDATE SPELLING DIFFICULTY CALCULATION METHOD
-- ============================================================================

-- Update spelling_difficulty_calculation_method (must be ≤50 chars)
UPDATE spelling_words
SET spelling_difficulty_calculation_method = 'XGBoost ML model v2025.01, 52% accuracy'
WHERE spelling_difficulty_level IS NOT NULL;

-- ============================================================================
-- STEP 2: UPDATE VOCABULARY DIFFICULTY CALCULATION METHOD  
-- ============================================================================

-- Update vocabulary_difficulty_calculation_method (must be ≤50 chars)
UPDATE spelling_words
SET vocabulary_difficulty_calculation_method = 'Zipf frequency bins: 6+,5-6,3-5,2-3,0-2'
WHERE vocabulary_difficulty_level IS NOT NULL;

-- ============================================================================
-- STEP 3: VERIFY UPDATES
-- ============================================================================

-- Check lengths to ensure they fit
SELECT 
    'Method field lengths:' as check,
    LENGTH('XGBoost ML model v2025.01, 52% accuracy') as spelling_method_length,
    LENGTH('Zipf frequency bins: 6+,5-6,3-5,2-3,0-2') as vocab_method_length;

-- Count how many records were updated
SELECT 
    'Records updated:' as info;

SELECT 
    'Spelling method' as field,
    COUNT(*) as updated_count,
    spelling_difficulty_calculation_method as method_value
FROM spelling_words
WHERE spelling_difficulty_calculation_method = 'XGBoost ML model v2025.01, 52% accuracy'
GROUP BY spelling_difficulty_calculation_method
UNION ALL
SELECT 
    'Vocabulary method' as field,
    COUNT(*) as updated_count,
    vocabulary_difficulty_calculation_method as method_value
FROM spelling_words
WHERE vocabulary_difficulty_calculation_method = 'Zipf frequency bins: 6+,5-6,3-5,2-3,0-2'
GROUP BY vocabulary_difficulty_calculation_method;

-- ============================================================================
-- STEP 4: CREATE DETAILED DOCUMENTATION VIEW
-- ============================================================================

-- Since the fields are limited to 50 chars, create a view with full details
CREATE OR REPLACE VIEW difficulty_methodology_detailed AS
SELECT 
    'Spelling Difficulty' as difficulty_type,
    'XGBoost ML model v2025.01, 52% accuracy' as method_short,
    'XGBoost Machine Learning Model trained on 9,866 bee-rated words. ' ||
    'Primary features: Zipf frequency (32.8% importance), word length (21.7%), ' ||
    'vowel count, syllable count, orthographic patterns. ' ||
    'Cross-validated accuracy: 48.1%. Scale: 1-5 (Very Easy to Very Hard).' as full_description,
    '2025-01-24' as last_updated
UNION ALL
SELECT 
    'Vocabulary Difficulty' as difficulty_type,
    'Zipf frequency bins: 6+,5-6,3-5,2-3,0-2' as method_short,
    'Frequency-based binning using Zipf scale from wordfreq library. ' ||
    'Level 1: freq≥6 (Basic/very common), Level 2: freq 5-6 (Elementary/common), ' ||
    'Level 3: freq 3-5 (Intermediate/moderate), Level 4: freq 2-3 (Advanced/rare), ' ||
    'Level 5: freq 0-2 (Expert/very rare). 100% deterministic mapping.' as full_description,
    '2025-01-24' as last_updated;

-- Display the methodology
SELECT * FROM difficulty_methodology_detailed;

-- ============================================================================
-- STEP 5: SHOW SAMPLE RESULTS
-- ============================================================================

SELECT 
    'Sample of updated records:' as info;

SELECT 
    word,
    spelling_difficulty_level as spell_lvl,
    vocabulary_difficulty_level as vocab_lvl,
    ROUND(frequency::numeric, 2) as freq,
    spelling_difficulty_calculation_method as spell_method,
    vocabulary_difficulty_calculation_method as vocab_method
FROM spelling_words
WHERE spelling_difficulty_calculation_method IS NOT NULL
    AND vocabulary_difficulty_calculation_method IS NOT NULL
ORDER BY RANDOM()
LIMIT 5;

-- ============================================================================
-- SUMMARY
-- ============================================================================

SELECT 
    'Update Complete' as status,
    COUNT(*) as total_records_updated
FROM spelling_words
WHERE spelling_difficulty_calculation_method = 'XGBoost ML model v2025.01, 52% accuracy'
    AND vocabulary_difficulty_calculation_method = 'Zipf frequency bins: 6+,5-6,3-5,2-3,0-2';