-- Update the language_vocabulary_with_difficulty view to include vocabulary_type column

-- Drop the existing view if it exists
DROP VIEW IF EXISTS language_vocabulary_with_difficulty;

-- Create the updated view with vocabulary_type included
CREATE VIEW language_vocabulary_with_difficulty AS
SELECT 
  lv.*,  -- All columns from language_vocabulary including vocabulary_type
  sdl.name as difficulty_name,
  sdl.description as difficulty_description,
  CASE 
    WHEN lv.cognate_note IS NOT NULL THEN true 
    ELSE false 
  END as is_cognate,
  CASE 
    WHEN lv.false_friend_warning IS NOT NULL THEN true 
    ELSE false 
  END as is_false_friend
FROM language_vocabulary lv
LEFT JOIN spelling_difficulty_levels sdl ON lv.difficulty_id = sdl.id;

-- Grant necessary permissions (adjust based on your needs)
GRANT SELECT ON language_vocabulary_with_difficulty TO anon;
GRANT SELECT ON language_vocabulary_with_difficulty TO authenticated;