-- Add category column to language_questions table
-- This will categorize questions as 'grammar', 'reading', or 'listening'

-- First, add the new category column with a CHECK constraint
ALTER TABLE language_questions 
ADD COLUMN IF NOT EXISTS category TEXT;

-- Add a check constraint to ensure only valid categories
ALTER TABLE language_questions 
ADD CONSTRAINT language_questions_category_check 
CHECK (category IN ('grammar', 'reading/listening'));

-- Update existing questions based on their type
-- For now, we'll set Latin questions as grammar and Spanish as grammar too
-- You can adjust this logic as needed
UPDATE language_questions 
SET category = 'grammar'
WHERE category IS NULL;

-- Make the column NOT NULL after populating it
ALTER TABLE language_questions 
ALTER COLUMN category SET NOT NULL;

-- Add an index for better query performance
CREATE INDEX IF NOT EXISTS idx_language_questions_category 
ON language_questions(language_id, category);

-- Add comment to explain the column
COMMENT ON COLUMN language_questions.category IS 'Question category: grammar or reading/listening (reading and listening share the same question content).';