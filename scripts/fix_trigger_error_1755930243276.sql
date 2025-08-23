-- Fix trigger error for missing ai_difficulty_level column
-- Generated on 2025-08-23T06:24:03.276Z

-- Option 1: Add missing columns if they don't exist
-- Uncomment these lines if you want to add the missing columns
-- ALTER TABLE spelling_words ADD COLUMN IF NOT EXISTS ai_difficulty_level INTEGER;
-- ALTER TABLE spelling_words ADD COLUMN IF NOT EXISTS ai_difficulty_name TEXT;

-- Option 2: Drop the problematic trigger (recommended for now)
-- This will remove the trigger that's causing the error
DROP TRIGGER IF EXISTS update_difficulty_name_trigger ON spelling_words;
DROP FUNCTION IF EXISTS update_difficulty_name();

-- Option 3: Recreate a safer trigger that only works with existing columns
-- This creates a new trigger that checks for column existence
CREATE OR REPLACE FUNCTION update_spelling_difficulty_name()
RETURNS TRIGGER AS $$
BEGIN
  -- Only update spelling difficulty name if spelling_difficulty_level exists and is not null
  IF NEW.spelling_difficulty_level IS NOT NULL THEN
    CASE NEW.spelling_difficulty_level
      WHEN 1 THEN NEW.spelling_difficulty_name := 'Beginner';
      WHEN 2 THEN NEW.spelling_difficulty_name := 'Elementary';
      WHEN 3 THEN NEW.spelling_difficulty_name := 'Intermediate';
      WHEN 4 THEN NEW.spelling_difficulty_name := 'Advanced';
      WHEN 5 THEN NEW.spelling_difficulty_name := 'Expert';
      ELSE NEW.spelling_difficulty_name := NULL;
    END CASE;
  END IF;
  
  -- Only update vocabulary difficulty name if vocabulary_difficulty_level exists and is not null
  IF NEW.vocabulary_difficulty_level IS NOT NULL THEN
    CASE NEW.vocabulary_difficulty_level
      WHEN 1 THEN NEW.vocabulary_difficulty_name := 'Basic';
      WHEN 2 THEN NEW.vocabulary_difficulty_name := 'Elementary';
      WHEN 3 THEN NEW.vocabulary_difficulty_name := 'Intermediate';
      WHEN 4 THEN NEW.vocabulary_difficulty_name := 'Advanced';
      WHEN 5 THEN NEW.vocabulary_difficulty_name := 'Expert';
      ELSE NEW.vocabulary_difficulty_name := NULL;
    END CASE;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the new safer trigger
CREATE TRIGGER update_spelling_difficulty_name_trigger
  BEFORE INSERT OR UPDATE ON spelling_words
  FOR EACH ROW
  EXECUTE FUNCTION update_spelling_difficulty_name();

-- Verify the trigger was created successfully
SELECT 
  trigger_name, 
  event_manipulation, 
  action_timing,
  action_statement
FROM information_schema.triggers 
WHERE event_object_table = 'spelling_words';