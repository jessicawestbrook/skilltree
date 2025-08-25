-- Cleanup script for invalid entries in spelling_words table
-- Run this in Supabase SQL editor

-- First, create a backup of the current data
CREATE TABLE IF NOT EXISTS spelling_words_bkp_invalid AS 
SELECT * FROM spelling_words 
WHERE id IN (
  '6817d6b8-2730-475c-8921-a17430f8d33a', -- aaccdi (invalid)
  'f8c38699-3ed5-4119-a559-974cbd1cdd86', -- dlailmnr (invalid)
  '18aefd86-92c5-4037-a544-0547fd5c9e32'  -- centennialcertiorari (combined)
);

-- Delete the invalid entries (not real words and combined words)
DELETE FROM spelling_words 
WHERE id IN (
  '6817d6b8-2730-475c-8921-a17430f8d33a', -- aaccdi (invalid)
  'f8c38699-3ed5-4119-a559-974cbd1cdd86', -- dlailmnr (invalid)
  '18aefd86-92c5-4037-a544-0547fd5c9e32'  -- centennialcertiorari (combined word, certiorari already exists separately)
);

-- Verify the cleanup
SELECT 'Cleanup Results:' as message;

SELECT 'Deleted invalid/combined words:' as action, COUNT(*) as count
FROM spelling_words_bkp_invalid
WHERE id IN ('6817d6b8-2730-475c-8921-a17430f8d33a', 'f8c38699-3ed5-4119-a559-974cbd1cdd86', '18aefd86-92c5-4037-a544-0547fd5c9e32');

-- Check if there are any other potential issues to review manually
SELECT 'Words to review manually:' as message;

SELECT word, LEFT(definition, 100) as definition_preview
FROM spelling_words
WHERE 
  -- Very long words that might be combined
  (LENGTH(word) > 25 AND word NOT LIKE '%-%' AND word NOT LIKE '% %')
  OR
  -- Words with unusual capitalization patterns
  (word ~ '[a-z][A-Z]')
ORDER BY LENGTH(word) DESC
LIMIT 10;