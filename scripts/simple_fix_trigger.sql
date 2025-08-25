-- Simple fix for the trigger error
-- The broken trigger is trying to set spelling_difficulty_name on the wrong table

-- Step 1: Drop the broken trigger and function
DROP TRIGGER IF EXISTS update_spelling_difficulty_name_trigger ON spelling_words CASCADE;
DROP TRIGGER IF EXISTS before_update_spelling_words ON spelling_words CASCADE;
DROP TRIGGER IF EXISTS after_update_spelling_words ON spelling_words CASCADE;
DROP FUNCTION IF EXISTS update_spelling_difficulty_name() CASCADE;

-- Step 2: If you need to maintain the relationship between 
-- spelling_difficulty_level (1-5) and spelling_difficulty_name,
-- create a proper lookup or use a CASE statement in views

-- Create a view that includes the difficulty name if needed:
CREATE OR REPLACE VIEW spelling_words_with_difficulty_names AS
SELECT 
    sw.*,
    CASE sw.spelling_difficulty_level
        WHEN 1 THEN 'Very Easy'
        WHEN 2 THEN 'Easy'
        WHEN 3 THEN 'Medium'
        WHEN 4 THEN 'Hard'
        WHEN 5 THEN 'Very Hard'
        ELSE 'Unknown'
    END AS spelling_difficulty_name,
    CASE sw.vocabulary_difficulty_level
        WHEN 1 THEN 'Basic'
        WHEN 2 THEN 'Elementary'
        WHEN 3 THEN 'Intermediate'
        WHEN 4 THEN 'Advanced'
        WHEN 5 THEN 'Expert'
        ELSE 'Unknown'
    END AS vocabulary_difficulty_name
FROM spelling_words sw;

-- Now you can update the frequency field without trigger errors
-- The view provides the difficulty names when needed