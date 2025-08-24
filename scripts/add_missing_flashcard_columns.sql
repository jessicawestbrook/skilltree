-- Add missing columns to user_flashcard_reviews table
-- Run this script in Supabase SQL editor

-- Add easiness_factor column (for spaced repetition algorithm)
ALTER TABLE user_flashcard_reviews 
ADD COLUMN IF NOT EXISTS easiness_factor DECIMAL(3,2) DEFAULT 2.5;

-- Add interval_days column (days until next review)
ALTER TABLE user_flashcard_reviews 
ADD COLUMN IF NOT EXISTS interval_days INTEGER DEFAULT 1;

-- Add consecutive_correct column (streak counter)
ALTER TABLE user_flashcard_reviews 
ADD COLUMN IF NOT EXISTS consecutive_correct INTEGER DEFAULT 0;

-- Add total_correct column (lifetime correct answers)
ALTER TABLE user_flashcard_reviews 
ADD COLUMN IF NOT EXISTS total_correct INTEGER DEFAULT 0;

-- Add total_attempts column (lifetime attempts)
ALTER TABLE user_flashcard_reviews 
ADD COLUMN IF NOT EXISTS total_attempts INTEGER DEFAULT 0;

-- Add created_at column if it doesn't exist
ALTER TABLE user_flashcard_reviews 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Add updated_at column if it doesn't exist
ALTER TABLE user_flashcard_reviews 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Create an index on user_id and next_review for efficient querying
CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_user_next_review 
ON user_flashcard_reviews(user_id, next_review);

-- Create an index on flashcard_type for filtering
CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_type 
ON user_flashcard_reviews(flashcard_type);

-- Add a trigger to automatically update the updated_at column
-- First drop the trigger if it exists
DROP TRIGGER IF EXISTS update_user_flashcard_reviews_updated_at ON user_flashcard_reviews;

-- Create or replace the function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create the trigger
CREATE TRIGGER update_user_flashcard_reviews_updated_at 
BEFORE UPDATE ON user_flashcard_reviews 
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();