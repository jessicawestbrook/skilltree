-- Update both spelling and vocabulary difficulties in spelling_words table
-- This script combines vocabulary frequency-based updates and XGBoost spelling predictions

-- ============================================================================
-- PART 1: UPDATE VOCABULARY DIFFICULTY BASED ON FREQUENCY BINS
-- ============================================================================

-- Create backup for vocabulary update
CREATE TABLE IF NOT EXISTS spelling_words_bkp_difficulties AS 
SELECT * FROM spelling_words;

-- Update vocabulary_difficulty_level based on frequency bins
UPDATE spelling_words 
SET vocabulary_difficulty_level = CASE
    WHEN frequency >= 6 THEN 1        -- Very common & Common (6+) -> Level 1 (Basic)
    WHEN frequency >= 5 THEN 2        -- Common (5-6) -> Level 2 (Elementary)
    WHEN frequency >= 3 THEN 3        -- Moderate & Uncommon (3-5) -> Level 3 (Intermediate)
    WHEN frequency >= 2 THEN 4        -- Rare (2-3) -> Level 4 (Advanced)
    WHEN frequency >= 0 THEN 5        -- Very rare (0-2) -> Level 5 (Expert)
    ELSE vocabulary_difficulty_level  -- Keep existing if frequency is NULL
END
WHERE frequency IS NOT NULL;

-- Show vocabulary update results
SELECT 
    'VOCABULARY DIFFICULTY UPDATE COMPLETE' as status,
    COUNT(*) as words_updated
FROM spelling_words
WHERE frequency IS NOT NULL;

-- ============================================================================
-- PART 2: UPDATE SPELLING DIFFICULTY FROM XGBOOST PREDICTIONS
-- ============================================================================

-- The spelling difficulty updates are in update_xgboost_predictions.sql
-- Run that file after this one, or include its contents here

-- ============================================================================
-- PART 3: VERIFY FINAL DISTRIBUTIONS
-- ============================================================================

-- Check final vocabulary distribution
SELECT 
    'Final Vocabulary Distribution' as analysis;

SELECT 
    vocabulary_difficulty_level as level,
    CASE vocabulary_difficulty_level
        WHEN 1 THEN '1: Basic (freq 6+)'
        WHEN 2 THEN '2: Elementary (5-6)'
        WHEN 3 THEN '3: Intermediate (3-5)'
        WHEN 4 THEN '4: Advanced (2-3)'
        WHEN 5 THEN '5: Expert (0-2)'
    END as description,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spelling_words WHERE vocabulary_difficulty_level IS NOT NULL), 1) as percentage
FROM spelling_words
WHERE vocabulary_difficulty_level IS NOT NULL
GROUP BY vocabulary_difficulty_level
ORDER BY vocabulary_difficulty_level;

-- Check spelling distribution (after XGBoost update)
SELECT 
    'Final Spelling Distribution' as analysis;

SELECT 
    spelling_difficulty_level as level,
    CASE spelling_difficulty_level
        WHEN 1 THEN '1: Very Easy'
        WHEN 2 THEN '2: Easy'
        WHEN 3 THEN '3: Medium'
        WHEN 4 THEN '4: Hard'
        WHEN 5 THEN '5: Very Hard'
    END as description,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spelling_words WHERE spelling_difficulty_level IS NOT NULL), 1) as percentage
FROM spelling_words
WHERE spelling_difficulty_level IS NOT NULL
GROUP BY spelling_difficulty_level
ORDER BY spelling_difficulty_level;

-- Show some example words at each difficulty combination
SELECT 
    'Example Words by Difficulty Combination' as info;

SELECT 
    spelling_difficulty_level as spell_lvl,
    vocabulary_difficulty_level as vocab_lvl,
    word,
    ROUND(frequency::numeric, 2) as freq
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY spelling_difficulty_level, vocabulary_difficulty_level ORDER BY RANDOM()) as rn
    FROM spelling_words
    WHERE spelling_difficulty_level IS NOT NULL 
    AND vocabulary_difficulty_level IS NOT NULL
    AND frequency IS NOT NULL
) t
WHERE rn = 1
ORDER BY spelling_difficulty_level, vocabulary_difficulty_level
LIMIT 25;

-- Summary statistics
SELECT 
    'Summary Statistics' as info,
    COUNT(*) as total_words,
    COUNT(spelling_difficulty_level) as words_with_spelling,
    COUNT(vocabulary_difficulty_level) as words_with_vocabulary,
    COUNT(frequency) as words_with_frequency,
    ROUND(AVG(spelling_difficulty_level)::numeric, 2) as avg_spelling_diff,
    ROUND(AVG(vocabulary_difficulty_level)::numeric, 2) as avg_vocab_diff,
    ROUND(AVG(frequency)::numeric, 2) as avg_frequency
FROM spelling_words;