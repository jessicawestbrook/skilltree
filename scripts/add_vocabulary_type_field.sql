-- Add vocabulary_type field to language_vocabulary table
-- This categorizes entries as 'word', 'character', or 'alphabet'

-- First, add the new vocabulary_type column
ALTER TABLE language_vocabulary 
ADD COLUMN IF NOT EXISTS vocabulary_type TEXT;

-- Add a check constraint to ensure only valid types
ALTER TABLE language_vocabulary 
DROP CONSTRAINT IF EXISTS language_vocabulary_type_check;

ALTER TABLE language_vocabulary 
ADD CONSTRAINT language_vocabulary_type_check 
CHECK (vocabulary_type IN ('word', 'character'));

-- Set default value for existing entries (all current entries are words)
UPDATE language_vocabulary 
SET vocabulary_type = 'word'
WHERE vocabulary_type IS NULL;

-- Make the column NOT NULL after populating it
ALTER TABLE language_vocabulary 
ALTER COLUMN vocabulary_type SET NOT NULL;

-- Set default for future insertions
ALTER TABLE language_vocabulary 
ALTER COLUMN vocabulary_type SET DEFAULT 'word';

-- Add an index for better query performance
CREATE INDEX IF NOT EXISTS idx_language_vocabulary_type 
ON language_vocabulary(language, vocabulary_type);

-- Add comment to explain the column
COMMENT ON COLUMN language_vocabulary.vocabulary_type IS 'Type of vocabulary entry: word (full words) or character (individual characters like Chinese/Japanese)';