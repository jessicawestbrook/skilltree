-- Add grade_level column to spelling_words table
ALTER TABLE spelling_words ADD COLUMN IF NOT EXISTS grade_level TEXT;

-- Verify column was added
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'spelling_words' 
AND column_name = 'grade_level';

-- Check if column exists by trying to update a non-existent record
UPDATE spelling_words 
SET grade_level = 'test' 
WHERE id = '00000000-0000-0000-0000-000000000000';