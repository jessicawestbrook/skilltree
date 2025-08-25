-- Fix the trigger to properly handle the foreign key relationship
-- spelling_difficulty_name is in a lookup table, not in spelling_words

-- First, let's understand the structure
-- Check if there's a spelling_difficulty lookup table
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name IN ('spelling_difficulty', 'spelling_difficulties', 'difficulty_levels')
AND table_schema = 'public'
ORDER BY table_name, ordinal_position;

-- Check the current structure of spelling_words
SELECT 
    column_name,
    data_type,
    column_default
FROM information_schema.columns
WHERE table_name = 'spelling_words'
AND column_name LIKE '%difficulty%'
ORDER BY ordinal_position;

-- Check foreign key constraints
SELECT
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND tc.table_name = 'spelling_words';

-- Now let's fix the trigger
-- First, drop the broken trigger
DROP TRIGGER IF EXISTS update_spelling_difficulty_name_trigger ON spelling_words CASCADE;
DROP FUNCTION IF EXISTS update_spelling_difficulty_name() CASCADE;

-- If you need a trigger to validate spelling_difficulty_level values,
-- here's a proper one that doesn't try to set a non-existent field:
CREATE OR REPLACE FUNCTION validate_spelling_difficulty_level()
RETURNS TRIGGER AS $$
BEGIN
    -- Validate that spelling_difficulty_level is between 1 and 5
    IF NEW.spelling_difficulty_level IS NOT NULL THEN
        IF NEW.spelling_difficulty_level < 1 OR NEW.spelling_difficulty_level > 5 THEN
            RAISE EXCEPTION 'spelling_difficulty_level must be between 1 and 5';
        END IF;
    END IF;
    
    -- Return the new record without trying to set non-existent fields
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the validation trigger (optional)
-- CREATE TRIGGER validate_spelling_difficulty_trigger
-- BEFORE INSERT OR UPDATE ON spelling_words
-- FOR EACH ROW
-- EXECUTE FUNCTION validate_spelling_difficulty_level();

-- If there IS a spelling_difficulty lookup table and you want to ensure
-- referential integrity, you should use a proper foreign key constraint instead:
-- ALTER TABLE spelling_words
-- ADD CONSTRAINT fk_spelling_difficulty_level
-- FOREIGN KEY (spelling_difficulty_level)
-- REFERENCES spelling_difficulty(level);

-- But for now, just removing the broken trigger should fix your immediate problem