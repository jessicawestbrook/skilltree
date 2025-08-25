-- Remove the broken trigger that's causing the error
-- This trigger is trying to update spelling_difficulty_name which doesn't exist

-- Drop any triggers related to spelling_difficulty_name
DROP TRIGGER IF EXISTS update_spelling_difficulty_name_trigger ON spelling_words CASCADE;
DROP TRIGGER IF EXISTS spelling_difficulty_name_trigger ON spelling_words CASCADE;
DROP TRIGGER IF EXISTS before_update_spelling_difficulty ON spelling_words CASCADE;
DROP TRIGGER IF EXISTS after_update_spelling_difficulty ON spelling_words CASCADE;

-- Drop the function that's causing the error
DROP FUNCTION IF EXISTS update_spelling_difficulty_name() CASCADE;

-- Verify the triggers are removed
SELECT 
    'Remaining triggers on spelling_words:' as info,
    COUNT(*) as count
FROM pg_trigger 
WHERE tgrelid = 'spelling_words'::regclass
AND NOT tgisinternal;

-- Now you can safely run your frequency updates
-- The error "record "new" has no field "spelling_difficulty_name"" should be gone