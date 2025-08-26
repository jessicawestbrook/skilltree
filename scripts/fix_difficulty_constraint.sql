-- ============================================================
-- Update difficulty constraint from 'average' to 'medium'
-- ============================================================
-- IMPORTANT: Run this script in Supabase SQL Editor
-- Go to: Your Supabase Dashboard > SQL Editor > New Query
-- ============================================================

-- Step 1: Create backup table (if not exists)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'questions_bkp_difficulty') THEN
        CREATE TABLE questions_bkp_difficulty AS SELECT * FROM questions;
        RAISE NOTICE 'Backup table created: questions_bkp_difficulty';
    ELSE
        RAISE NOTICE 'Backup table already exists: questions_bkp_difficulty';
    END IF;
END $$;

-- Step 2: Show current distribution
SELECT 'Current distribution:' as info;
SELECT difficulty, COUNT(*) as count 
FROM questions 
WHERE difficulty IS NOT NULL
GROUP BY difficulty 
ORDER BY difficulty;

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
SELECT 'Updated distribution:' as info;
SELECT difficulty, COUNT(*) as count 
FROM questions 
WHERE difficulty IS NOT NULL
GROUP BY difficulty 
ORDER BY difficulty;

-- Step 7: Test the constraint
-- This should work:
DO $$ 
DECLARE
    test_id UUID;
BEGIN
    SELECT id INTO test_id FROM questions WHERE difficulty = 'medium' LIMIT 1;
    IF test_id IS NOT NULL THEN
        UPDATE questions SET difficulty = 'medium' WHERE id = test_id;
        RAISE NOTICE 'Test 1 passed: Can set difficulty to medium';
    END IF;
END $$;

-- This should fail (uncomment to test):
-- UPDATE questions SET difficulty = 'average' WHERE id = (SELECT id FROM questions LIMIT 1);

-- Step 8: Summary
SELECT 
    'UPDATE COMPLETE' as status,
    COUNT(*) FILTER (WHERE difficulty = 'easy') as easy_count,
    COUNT(*) FILTER (WHERE difficulty = 'medium') as medium_count,
    COUNT(*) FILTER (WHERE difficulty = 'hard') as hard_count,
    COUNT(*) as total_count
FROM questions;