-- Update difficulty constraint from 'average' to 'medium'
-- Run this script in Supabase SQL Editor

-- Step 1: Create backup of questions table
CREATE TABLE IF NOT EXISTS questions_bkp_20250825 AS SELECT * FROM questions;

-- Step 2: Verify backup was created
SELECT COUNT(*) as backup_count FROM questions_bkp_20250825;

-- Step 3: Drop the existing constraint
ALTER TABLE questions 
DROP CONSTRAINT IF EXISTS questions_difficulty_check;

-- Step 4: Update all 'average' values to 'medium'
UPDATE questions 
SET difficulty = 'medium' 
WHERE difficulty = 'average';

-- Step 5: Add the new constraint with 'medium' instead of 'average'
ALTER TABLE questions 
ADD CONSTRAINT questions_difficulty_check 
CHECK (difficulty IN ('easy', 'medium', 'hard'));

-- Step 6: Verify the update
SELECT difficulty, COUNT(*) as count 
FROM questions 
GROUP BY difficulty 
ORDER BY difficulty;

-- Step 7: Verify constraint is working
-- This should succeed:
-- UPDATE questions SET difficulty = 'medium' WHERE id = (SELECT id FROM questions LIMIT 1);

-- This should fail:
-- UPDATE questions SET difficulty = 'average' WHERE id = (SELECT id FROM questions LIMIT 1);