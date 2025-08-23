-- Create backup table before updating
-- Generated on 2025-08-23T05:59:14.885Z

-- Create backup table
CREATE TABLE spelling_words_bkp AS SELECT * FROM spelling_words;

-- Verify backup was created
SELECT 
  'bkp' as backup_name,
  COUNT(*) as word_count,
  COUNT(DISTINCT source_difficulty) as unique_difficulties,
  MIN(created_at) as oldest_entry,
  MAX(created_at) as newest_entry
FROM spelling_words_bkp;