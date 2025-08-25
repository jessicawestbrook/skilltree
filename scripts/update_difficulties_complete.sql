-- Complete SQL script to update both spelling and vocabulary difficulties
-- Run this entire file in your SQL console

-- ============================================================================
-- STEP 1: CREATE BACKUP
-- ============================================================================

CREATE TABLE IF NOT EXISTS spelling_words_bkp_complete_update AS 
SELECT * FROM spelling_words;

-- ============================================================================
-- STEP 2: UPDATE VOCABULARY DIFFICULTY BASED ON FREQUENCY
-- ============================================================================

UPDATE spelling_words 
SET vocabulary_difficulty_level = CASE
    WHEN frequency >= 6 THEN 1        -- Very common (6+) -> Level 1 (Basic)
    WHEN frequency >= 5 THEN 2        -- Common (5-6) -> Level 2 (Elementary)
    WHEN frequency >= 3 THEN 3        -- Moderate/Uncommon (3-5) -> Level 3 (Intermediate)
    WHEN frequency >= 2 THEN 4        -- Rare (2-3) -> Level 4 (Advanced)
    WHEN frequency >= 0 THEN 5        -- Very rare (0-2) -> Level 5 (Expert)
    ELSE vocabulary_difficulty_level  -- Keep existing if frequency is NULL
END
WHERE frequency IS NOT NULL;

-- Show vocabulary update results
SELECT 'Vocabulary Update Complete' as status,
       COUNT(*) as words_updated
FROM spelling_words
WHERE frequency IS NOT NULL;

-- ============================================================================
-- STEP 3: CHECK DISTRIBUTIONS AFTER UPDATE
-- ============================================================================

-- Check vocabulary distribution
SELECT 
    vocabulary_difficulty_level as level,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spelling_words WHERE vocabulary_difficulty_level IS NOT NULL), 1) as percentage,
    ROUND(AVG(frequency)::numeric, 2) as avg_frequency
FROM spelling_words
WHERE vocabulary_difficulty_level IS NOT NULL
GROUP BY vocabulary_difficulty_level
ORDER BY vocabulary_difficulty_level;

-- Check spelling distribution (current state)
SELECT 
    spelling_difficulty_level as level,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spelling_words WHERE spelling_difficulty_level IS NOT NULL), 1) as percentage
FROM spelling_words
WHERE spelling_difficulty_level IS NOT NULL
GROUP BY spelling_difficulty_level
ORDER BY spelling_difficulty_level;

-- ============================================================================
-- STEP 4: SHOW SAMPLE WORDS
-- ============================================================================

-- Show examples of vocabulary levels with their frequencies
SELECT 'Vocabulary Level Examples:' as info;

SELECT 
    vocabulary_difficulty_level,
    word,
    ROUND(frequency::numeric, 2) as freq
FROM (
    SELECT vocabulary_difficulty_level, word, frequency,
           ROW_NUMBER() OVER (PARTITION BY vocabulary_difficulty_level ORDER BY RANDOM()) as rn
    FROM spelling_words
    WHERE vocabulary_difficulty_level IS NOT NULL
    AND frequency IS NOT NULL
) t
WHERE rn <= 3
ORDER BY vocabulary_difficulty_level, word;

-- ============================================================================
-- NOTE: To update spelling difficulties with XGBoost predictions,
-- run the update_xgboost_predictions.sql file separately
-- ============================================================================