-- Update vocabulary_difficulty_level based on frequency bins
-- This maps Zipf frequency to 5 difficulty levels for vocabulary learning

-- Create backup first
CREATE TABLE IF NOT EXISTS spelling_words_bkp_vocab_freq AS 
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

-- Verify the update
SELECT 
    'Vocabulary Difficulty Distribution (Frequency-Based)' as analysis;

SELECT 
    vocabulary_difficulty_level,
    CASE vocabulary_difficulty_level
        WHEN 1 THEN 'Basic (6+)'
        WHEN 2 THEN 'Elementary (5-6)'
        WHEN 3 THEN 'Intermediate (3-5)'
        WHEN 4 THEN 'Advanced (2-3)'
        WHEN 5 THEN 'Expert (0-2)'
        ELSE 'Unknown'
    END as level_description,
    COUNT(*) as word_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spelling_words WHERE frequency IS NOT NULL), 1) as percentage,
    ROUND(AVG(frequency)::numeric, 2) as avg_frequency
FROM spelling_words
WHERE frequency IS NOT NULL
GROUP BY vocabulary_difficulty_level
ORDER BY vocabulary_difficulty_level;

-- Show some examples at each level
SELECT 'Examples by vocabulary level:' as info;

SELECT vocabulary_difficulty_level, word, frequency 
FROM (
    SELECT vocabulary_difficulty_level, word, frequency,
           ROW_NUMBER() OVER (PARTITION BY vocabulary_difficulty_level ORDER BY RANDOM()) as rn
    FROM spelling_words
    WHERE frequency IS NOT NULL
) t
WHERE rn <= 3
ORDER BY vocabulary_difficulty_level, word;