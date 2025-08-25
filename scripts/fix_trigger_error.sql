-- Fix trigger error for spelling_difficulty_name field
-- The trigger is trying to update a field that doesn't exist

-- First, let's check what triggers exist on the spelling_words table
SELECT 
    tgname AS trigger_name,
    tgtype,
    proname AS function_name
FROM pg_trigger t
JOIN pg_proc p ON t.tgfoid = p.oid
WHERE tgrelid = 'spelling_words'::regclass;

-- Check if the column exists
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'spelling_words' 
AND column_name LIKE '%difficulty%'
ORDER BY ordinal_position;

-- Look at the trigger function definition
SELECT prosrc 
FROM pg_proc 
WHERE proname = 'update_spelling_difficulty_name';

-- If the trigger is trying to update a non-existent column, we have options:

-- Option 1: Drop the trigger if it's not needed
-- DROP TRIGGER IF EXISTS update_spelling_difficulty_name_trigger ON spelling_words;
-- DROP FUNCTION IF EXISTS update_spelling_difficulty_name();

-- Option 2: Add the missing column if it's needed
-- ALTER TABLE spelling_words 
-- ADD COLUMN IF NOT EXISTS spelling_difficulty_name VARCHAR(50);

-- Option 3: Fix the trigger to not reference the non-existent column
-- This would require recreating the function

-- Let's create a script to safely handle this
DO $$
BEGIN
    -- Check if the column exists
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'spelling_words' 
        AND column_name = 'spelling_difficulty_name'
    ) THEN
        -- Check if trigger exists
        IF EXISTS (
            SELECT 1 
            FROM pg_trigger 
            WHERE tgname LIKE '%spelling_difficulty_name%' 
            AND tgrelid = 'spelling_words'::regclass
        ) THEN
            -- Drop the trigger since the column doesn't exist
            RAISE NOTICE 'Dropping trigger that references non-existent column spelling_difficulty_name';
            
            -- Find and drop all triggers that might reference this
            FOR r IN 
                SELECT tgname 
                FROM pg_trigger 
                WHERE tgrelid = 'spelling_words'::regclass
                AND tgname LIKE '%spelling_difficulty%'
            LOOP
                EXECUTE 'DROP TRIGGER IF EXISTS ' || r.tgname || ' ON spelling_words';
                RAISE NOTICE 'Dropped trigger: %', r.tgname;
            END LOOP;
            
            -- Drop the function too
            DROP FUNCTION IF EXISTS update_spelling_difficulty_name() CASCADE;
            RAISE NOTICE 'Dropped function update_spelling_difficulty_name()';
        END IF;
    ELSE
        RAISE NOTICE 'Column spelling_difficulty_name exists, trigger should work';
    END IF;
END $$;

-- After fixing, try the update again
-- The frequency update should now work without trigger errors