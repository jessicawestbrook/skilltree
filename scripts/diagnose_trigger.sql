-- Diagnose the trigger issue

-- 1. List all columns in spelling_words table
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'spelling_words'
AND column_name LIKE '%difficulty%'
ORDER BY ordinal_position;

-- 2. List all triggers on spelling_words
SELECT 
    trigger_name,
    event_manipulation,
    event_object_table,
    action_statement
FROM information_schema.triggers
WHERE event_object_table = 'spelling_words';

-- 3. Get the problematic trigger function source
\sf update_spelling_difficulty_name

-- 4. Simple fix - drop the problematic trigger and function
DROP TRIGGER IF EXISTS update_spelling_difficulty_name_trigger ON spelling_words;
DROP TRIGGER IF EXISTS spelling_difficulty_name_trigger ON spelling_words;
DROP TRIGGER IF EXISTS update_difficulty_name_trigger ON spelling_words;
DROP FUNCTION IF EXISTS update_spelling_difficulty_name() CASCADE;

-- 5. Verify triggers are gone
SELECT COUNT(*) as remaining_triggers
FROM information_schema.triggers
WHERE event_object_table = 'spelling_words'
AND trigger_name LIKE '%difficulty_name%';