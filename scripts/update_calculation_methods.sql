-- Update the calculation method fields to document how difficulties were calculated
-- This provides transparency about the methodology used

-- ============================================================================
-- STEP 1: UPDATE SPELLING DIFFICULTY CALCULATION METHOD
-- ============================================================================

-- Update spelling_difficulty_calculation_method to reflect XGBoost model
UPDATE spelling_words
SET spelling_difficulty_calculation_method = 
    'XGBoost ML model (v2025.01) trained on 9,866 bee-rated words. ' ||
    'Features: Zipf frequency (32.8% importance), word length (21.7%), ' ||
    'vowel count, syllable count, orthographic patterns. ' ||
    'Model accuracy: 52.38% (cross-validated: 48.1%). ' ||
    'Predictions mapped to 1-5 scale.'
WHERE spelling_difficulty_level IS NOT NULL;

-- ============================================================================
-- STEP 2: UPDATE VOCABULARY DIFFICULTY CALCULATION METHOD
-- ============================================================================

-- Update vocabulary_difficulty_calculation_method to reflect frequency binning
UPDATE spelling_words
SET vocabulary_difficulty_calculation_method = 
    'Frequency-based binning using Zipf scale from wordfreq library. ' ||
    'Level 1: freq≥6 (very common), Level 2: freq 5-6 (common), ' ||
    'Level 3: freq 3-5 (moderate/uncommon), Level 4: freq 2-3 (rare), ' ||
    'Level 5: freq 0-2 (very rare). ' ||
    'Updated: 2025-01-24'
WHERE vocabulary_difficulty_level IS NOT NULL;

-- ============================================================================
-- STEP 3: VERIFY UPDATES
-- ============================================================================

-- Check that methods were updated
SELECT 
    'Calculation Methods Updated' as status;

-- Count how many records have each method
SELECT 
    'Records with calculation methods:' as info;

SELECT 
    'Spelling method populated' as field,
    COUNT(*) as count
FROM spelling_words
WHERE spelling_difficulty_calculation_method IS NOT NULL
    AND spelling_difficulty_calculation_method LIKE '%XGBoost%'
UNION ALL
SELECT 
    'Vocabulary method populated' as field,
    COUNT(*) as count
FROM spelling_words
WHERE vocabulary_difficulty_calculation_method IS NOT NULL
    AND vocabulary_difficulty_calculation_method LIKE '%Frequency-based%';

-- Show a sample to verify
SELECT 
    'Sample of updated methods:' as info;

SELECT 
    word,
    spelling_difficulty_level,
    vocabulary_difficulty_level,
    ROUND(frequency::numeric, 2) as freq,
    LEFT(spelling_difficulty_calculation_method, 50) || '...' as spell_method_preview,
    LEFT(vocabulary_difficulty_calculation_method, 50) || '...' as vocab_method_preview
FROM spelling_words
WHERE spelling_difficulty_calculation_method IS NOT NULL
    AND vocabulary_difficulty_calculation_method IS NOT NULL
ORDER BY RANDOM()
LIMIT 3;

-- ============================================================================
-- STEP 4: ADDITIONAL DOCUMENTATION
-- ============================================================================

-- Create a summary view that explains the difficulty system
CREATE OR REPLACE VIEW difficulty_methodology AS
SELECT 
    'Spelling Difficulty' as difficulty_type,
    'XGBoost Machine Learning Model' as method,
    '1-5 (Very Easy to Very Hard)' as scale,
    '52.38%' as accuracy,
    '2025-01-24' as last_updated,
    'Trained on 9,866 words with bee ratings. Primary features: word frequency (32.8%), length (21.7%), orthographic complexity' as details
UNION ALL
SELECT 
    'Vocabulary Difficulty' as difficulty_type,
    'Frequency-Based Binning' as method,
    '1-5 (Basic to Expert)' as scale,
    '100%' as accuracy,
    '2025-01-24' as last_updated,
    'Based on Zipf frequency scale. Level 1: 6+ (very common), Level 2: 5-6, Level 3: 3-5, Level 4: 2-3, Level 5: 0-2 (very rare)' as details;

-- Display the methodology
SELECT * FROM difficulty_methodology;

-- ============================================================================
-- SUMMARY
-- ============================================================================

SELECT 
    'Update Complete' as status,
    'Both calculation method fields have been updated to reflect current methodology' as message;