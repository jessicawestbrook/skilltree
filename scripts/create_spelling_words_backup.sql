-- Check existing backup tables and create new backup
-- This will create spelling_words_bkp or spelling_words_bkp2, etc.

-- Create backup table (adjust the name if _bkp already exists)
CREATE TABLE spelling_words_bkp AS 
SELECT * FROM spelling_words;

-- Verify the backup
SELECT 
    (SELECT COUNT(*) FROM spelling_words) as original_count,
    (SELECT COUNT(*) FROM spelling_words_bkp) as backup_count;