-- Script to fix trigger issue and apply parts of speech updates
-- The error "record 'new' has no field 'spelling_difficulty_name'" indicates
-- a trigger is trying to access a field that doesn't exist

-- Step 1: Check for problematic triggers
SELECT 
    trigger_name,
    event_manipulation,
    event_object_table,
    action_statement
FROM information_schema.triggers 
WHERE event_object_table = 'spelling_words';

-- Step 2: Check if there are any functions that might be causing issues
SELECT 
    proname AS function_name,
    prosrc AS function_source
FROM pg_proc
WHERE prosrc LIKE '%spelling_difficulty_name%';

-- Step 3: Option A - Temporarily disable the trigger (if found)
-- ALTER TABLE spelling_words DISABLE TRIGGER [trigger_name];

-- Step 3: Option B - Fix the trigger to use correct column name
-- The trigger likely needs to reference 'ai_spelling_difficulty_name' instead of 'spelling_difficulty_name'

-- Step 4: Apply a test update
UPDATE spelling_words 
SET part_of_speech = 'verb' 
WHERE word = 'sound'
RETURNING word, part_of_speech;

-- Step 5: If test succeeds, run batch updates (first 100 as test)
BEGIN;

UPDATE spelling_words SET part_of_speech = 'verb' WHERE id = 'b45f74f4-a268-40af-af15-9d7aa93ae47c' AND part_of_speech IS NULL;
UPDATE spelling_words SET part_of_speech = 'verb' WHERE id = '005c6694-875c-4c22-aa04-76c56ca36373' AND part_of_speech IS NULL;
UPDATE spelling_words SET part_of_speech = 'noun' WHERE id = '00a7351a-ad32-4011-af5b-9da8fac7a391' AND part_of_speech IS NULL;

-- Check if updates worked
SELECT COUNT(*) as updated_count 
FROM spelling_words 
WHERE part_of_speech IS NOT NULL;

COMMIT;

-- Step 6: Re-enable trigger if it was disabled
-- ALTER TABLE spelling_words ENABLE TRIGGER [trigger_name];

-- Alternative approach: Create a temporary function to bypass triggers
CREATE OR REPLACE FUNCTION update_parts_of_speech() RETURNS void AS $$
BEGIN
    -- Disable triggers temporarily within this function
    ALTER TABLE spelling_words DISABLE TRIGGER ALL;
    
    -- Run your updates here
    UPDATE spelling_words SET part_of_speech = 'verb' WHERE id = 'b45f74f4-a268-40af-af15-9d7aa93ae47c';
    -- ... more updates
    
    -- Re-enable triggers
    ALTER TABLE spelling_words ENABLE TRIGGER ALL;
END;
$$ LANGUAGE plpgsql;

-- Then call: SELECT update_parts_of_speech();