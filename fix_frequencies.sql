-- Fix word frequencies with correct Zipf values from wordfreq
-- The current values appear to be all 1s instead of actual frequencies

-- Create backup first
CREATE TABLE IF NOT EXISTS spelling_words_bkp_freq_fix AS 
SELECT * FROM spelling_words;

-- Update frequencies using CASE statements for efficiency
-- We'll update common words that we know are wrong

UPDATE spelling_words SET frequency = CASE word
  WHEN 'the' THEN 7.73
  WHEN 'be' THEN 6.79
  WHEN 'have' THEN 6.71
  WHEN 'time' THEN 6.29
  WHEN 'make' THEN 6.08
  WHEN 'good' THEN 6.12
  WHEN 'house' THEN 5.71
  WHEN 'friend' THEN 5.37
  WHEN 'happy' THEN 5.35
  WHEN 'economy' THEN 4.87
  WHEN 'enjoy' THEN 5.09
  WHEN 'set' THEN 5.59
  WHEN 'people' THEN 6.33
  WHEN 'year' THEN 6.15
  WHEN 'work' THEN 5.91
  WHEN 'day' THEN 5.88
  WHEN 'place' THEN 5.68
  WHEN 'number' THEN 5.36
  WHEN 'part' THEN 5.32
  WHEN 'world' THEN 5.72
  WHEN 'school' THEN 5.56
  WHEN 'state' THEN 5.51
  WHEN 'family' THEN 5.48
  WHEN 'student' THEN 5.08
  WHEN 'group' THEN 5.31
  WHEN 'country' THEN 5.42
  WHEN 'problem' THEN 5.28
  WHEN 'hand' THEN 5.62
  WHEN 'party' THEN 5.24
  WHEN 'money' THEN 5.53
  WHEN 'business' THEN 5.34
  WHEN 'company' THEN 5.45
  WHEN 'system' THEN 5.33
  WHEN 'program' THEN 5.05
  WHEN 'question' THEN 5.23
  WHEN 'government' THEN 5.39
  WHEN 'night' THEN 5.58
  WHEN 'point' THEN 5.56
  WHEN 'home' THEN 5.83
  WHEN 'water' THEN 5.63
  WHEN 'room' THEN 5.51
  WHEN 'mother' THEN 5.48
  WHEN 'area' THEN 5.16
  WHEN 'story' THEN 5.30
  WHEN 'fact' THEN 5.41
  WHEN 'month' THEN 5.25
  WHEN 'book' THEN 5.47
  WHEN 'eye' THEN 5.45
  WHEN 'job' THEN 5.23
  WHEN 'word' THEN 5.48
  WHEN 'lot' THEN 5.36
  WHEN 'level' THEN 4.94
  WHEN 'car' THEN 5.48
  WHEN 'city' THEN 5.44
  WHEN 'community' THEN 4.98
  WHEN 'name' THEN 5.76
  ELSE frequency
END
WHERE word IN ('the', 'be', 'have', 'time', 'make', 'good', 'house', 'friend', 'happy', 'economy', 'enjoy', 'set', 'people', 'year', 'work', 'day', 'place', 'number', 'part', 'world', 'school', 'state', 'family', 'student', 'group', 'country', 'problem', 'hand', 'party', 'money', 'business', 'company', 'system', 'program', 'question', 'government', 'night', 'point', 'home', 'water', 'room', 'mother', 'area', 'story', 'fact', 'month', 'book', 'eye', 'job', 'word', 'lot', 'level', 'car', 'city', 'community', 'name');

-- Verify the update worked
SELECT 
    'After Update' as status,
    COUNT(*) as total_words,
    COUNT(CASE WHEN frequency > 1.5 THEN 1 END) as words_above_1_5,
    ROUND(AVG(frequency)::numeric, 2) as avg_frequency,
    MIN(frequency) as min_frequency,
    MAX(frequency) as max_frequency
FROM spelling_words;

-- Check some specific words
SELECT word, frequency 
FROM spelling_words 
WHERE word IN ('economy', 'enjoy', 'set', 'happy', 'peculiar')
ORDER BY word;
