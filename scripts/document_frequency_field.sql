-- Document the frequency field in spelling_words table
-- This field contains raw Zipf frequency values from the wordfreq library

-- Add comment to document the field if not already present
COMMENT ON COLUMN spelling_words.frequency IS 
'Zipf frequency from wordfreq library (0-8 scale where higher = more common). 
Scale: 7-8: Extremely common (the, be), 6-7: Very common (have, make), 
5-6: Common (house, friend), 4-5: Moderate (special, garden), 
3-4: Uncommon (peculiar, monastery), 2-3: Rare (perspicacious), 
0-2: Very rare (sesquipedalian). 
Most spelling bee words (80%) are very rare (0-2).';

-- Verify the frequency data
SELECT 
    'Frequency Distribution' as analysis,
    COUNT(*) as total_words,
    COUNT(frequency) as words_with_frequency,
    ROUND(AVG(frequency)::numeric, 2) as avg_frequency,
    MIN(frequency) as min_frequency,
    MAX(frequency) as max_frequency
FROM spelling_words;

-- Show distribution by frequency bands
SELECT 
    CASE 
        WHEN frequency >= 7 THEN '7-8: Extremely common'
        WHEN frequency >= 6 THEN '6-7: Very common'
        WHEN frequency >= 5 THEN '5-6: Common'
        WHEN frequency >= 4 THEN '4-5: Moderate'
        WHEN frequency >= 3 THEN '3-4: Uncommon'
        WHEN frequency >= 2 THEN '2-3: Rare'
        WHEN frequency >= 0 THEN '0-2: Very rare'
        ELSE 'NULL'
    END as frequency_band,
    COUNT(*) as word_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spelling_words), 1) as percentage
FROM spelling_words
GROUP BY frequency_band
ORDER BY 
    CASE frequency_band
        WHEN '7-8: Extremely common' THEN 1
        WHEN '6-7: Very common' THEN 2
        WHEN '5-6: Common' THEN 3
        WHEN '4-5: Moderate' THEN 4
        WHEN '3-4: Uncommon' THEN 5
        WHEN '2-3: Rare' THEN 6
        WHEN '0-2: Very rare' THEN 7
        ELSE 8
    END;