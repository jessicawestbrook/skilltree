-- Add quiz_score column to user_progress table if it doesn't exist
ALTER TABLE user_progress 
ADD COLUMN IF NOT EXISTS quiz_score NUMERIC(5,2) DEFAULT 0;

-- Update any existing records to have a default quiz_score if needed
UPDATE user_progress 
SET quiz_score = 75 
WHERE quiz_score IS NULL;