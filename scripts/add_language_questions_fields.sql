-- Add missing fields to language_questions table for Anki import
-- Run this before importing the Spanish grammar questions

-- Add new columns to language_questions table
ALTER TABLE language_questions 
ADD COLUMN IF NOT EXISTS correct_answer TEXT,
ADD COLUMN IF NOT EXISTS hint TEXT,
ADD COLUMN IF NOT EXISTS tags TEXT[],
ADD COLUMN IF NOT EXISTS estimated_time_seconds INTEGER,
ADD COLUMN IF NOT EXISTS metadata JSONB;

-- Update difficulty_level to accept text values temporarily
-- We'll convert: Elementary=2, Intermediate=3, Advanced=4
ALTER TABLE language_questions 
ALTER COLUMN difficulty_level TYPE VARCHAR(50) USING difficulty_level::VARCHAR;

-- Add index on tags for better searching
CREATE INDEX IF NOT EXISTS idx_language_questions_tags ON language_questions USING GIN (tags);

-- Add index on metadata for JSONB queries
CREATE INDEX IF NOT EXISTS idx_language_questions_metadata ON language_questions USING GIN (metadata);

-- Comment on new columns
COMMENT ON COLUMN language_questions.correct_answer IS 'Text answer for fill-in-blank questions';
COMMENT ON COLUMN language_questions.hint IS 'Hint to help users answer the question';
COMMENT ON COLUMN language_questions.tags IS 'Array of tags for categorization and filtering';
COMMENT ON COLUMN language_questions.estimated_time_seconds IS 'Estimated time to answer in seconds';
COMMENT ON COLUMN language_questions.metadata IS 'Additional structured data (verb, tense, person, source info, etc.)';