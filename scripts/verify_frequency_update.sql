-- Verify the frequency update worked correctly
-- Fixed version without the ORDER BY error

-- Check overall statistics
SELECT 
    'Frequency Statistics' as analysis,
    COUNT(*) as total_words,
    COUNT(frequency) as words_with_frequency,
    ROUND(AVG(frequency)::numeric, 2) as avg_frequency,
    MIN(frequency) as min_frequency,
    MAX(frequency) as max_frequency
FROM spelling_words;

-- Show distribution by frequency bands (fixed ORDER BY)
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
GROUP BY 
    CASE 
        WHEN frequency >= 7 THEN '7-8: Extremely common'
        WHEN frequency >= 6 THEN '6-7: Very common'
        WHEN frequency >= 5 THEN '5-6: Common'
        WHEN frequency >= 4 THEN '4-5: Moderate'
        WHEN frequency >= 3 THEN '3-4: Uncommon'
        WHEN frequency >= 2 THEN '2-3: Rare'
        WHEN frequency >= 0 THEN '0-2: Very rare'
        ELSE 'NULL'
    END
ORDER BY 
    MIN(frequency) DESC;

-- Check specific words that should have been updated
SELECT word, frequency 
FROM spelling_words 
WHERE word IN ('the', 'economy', 'enjoy', 'set', 'happy', 'peculiar', 'sesquipedalian', 'time', 'make', 'good')
ORDER BY frequency DESC;

-- Check if we still have the problem of everything being 1
SELECT 
    'Words with frequency = 1' as check,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spelling_words), 1) as percentage
FROM spelling_words
WHERE frequency = 1;

-- Sample of words at different frequency levels
SELECT 'Sample words by frequency:' as info;

SELECT word, frequency FROM spelling_words 
WHERE frequency BETWEEN 5.5 AND 6.5 
LIMIT 5;

SELECT word, frequency FROM spelling_words 
WHERE frequency BETWEEN 4.5 AND 5.5 
LIMIT 5;

SELECT word, frequency FROM spelling_words 
WHERE frequency BETWEEN 3.5 AND 4.5 
LIMIT 5;

SELECT word, frequency FROM spelling_words 
WHERE frequency BETWEEN 2.5 AND 3.5 
LIMIT 5;

SELECT word, frequency FROM spelling_words 
WHERE frequency BETWEEN 1.5 AND 2.5 
LIMIT 5;

SELECT word, frequency FROM spelling_words 
WHERE frequency < 1.5 
LIMIT 5;