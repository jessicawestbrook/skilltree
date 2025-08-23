-- Add created_at and updated_at columns to user_progress table
-- Run this in Supabase SQL editor before running add_money_counting_progress.sql

-- Add created_at column if it doesn't exist
ALTER TABLE user_progress 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Add updated_at column if it doesn't exist
ALTER TABLE user_progress 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Update existing rows to have timestamps if they're null
UPDATE user_progress 
SET created_at = COALESCE(created_at, last_accessed, NOW()),
    updated_at = COALESCE(updated_at, last_accessed, NOW())
WHERE created_at IS NULL OR updated_at IS NULL;

-- Verify the columns were added
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user_progress'
AND column_name IN ('created_at', 'updated_at')
ORDER BY column_name;