-- Add is_spelling_word and is_vocabulary_word flags to spelling_words table

-- Add the new columns with default value true
ALTER TABLE spelling_words 
ADD COLUMN IF NOT EXISTS is_spelling_word BOOLEAN DEFAULT true;

ALTER TABLE spelling_words 
ADD COLUMN IF NOT EXISTS is_vocabulary_word BOOLEAN DEFAULT true;

-- Update all existing records to have both flags set to true
UPDATE spelling_words 
SET is_spelling_word = true, 
    is_vocabulary_word = true
WHERE is_spelling_word IS NULL OR is_vocabulary_word IS NULL;

-- Create indexes for faster filtering
CREATE INDEX IF NOT EXISTS idx_spelling_words_is_spelling ON spelling_words(is_spelling_word) WHERE is_spelling_word = true;
CREATE INDEX IF NOT EXISTS idx_spelling_words_is_vocabulary ON spelling_words(is_vocabulary_word) WHERE is_vocabulary_word = true;