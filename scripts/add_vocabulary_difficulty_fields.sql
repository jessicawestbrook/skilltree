-- Add vocabulary difficulty fields to spelling_words table
-- First create backup, then rename existing fields and add new vocabulary fields

-- Step 1: Create backup table
CREATE TABLE IF NOT EXISTS spelling_words_bkp AS SELECT * FROM spelling_words;

-- Step 2: Rename existing difficulty fields to clarify they are spelling difficulties
ALTER TABLE spelling_words RENAME COLUMN difficulty_level TO spelling_difficulty_level;
ALTER TABLE spelling_words RENAME COLUMN difficulty_name TO spelling_difficulty_name;
ALTER TABLE spelling_words RENAME COLUMN ai_difficulty_level TO ai_spelling_difficulty_level;
ALTER TABLE spelling_words RENAME COLUMN ai_difficulty_name TO ai_spelling_difficulty_name;
ALTER TABLE spelling_words RENAME COLUMN difficulty_calculation_method TO spelling_difficulty_calculation_method;

-- Step 3: Add new vocabulary difficulty fields
ALTER TABLE spelling_words ADD COLUMN vocabulary_difficulty_level INTEGER;
ALTER TABLE spelling_words ADD COLUMN vocabulary_difficulty_name TEXT;
ALTER TABLE spelling_words ADD COLUMN vocabulary_semantic_complexity_score INTEGER;
ALTER TABLE spelling_words ADD COLUMN vocabulary_contextual_frequency_score INTEGER;
ALTER TABLE spelling_words ADD COLUMN vocabulary_conceptual_sophistication_score INTEGER;
ALTER TABLE spelling_words ADD COLUMN vocabulary_register_specificity_score INTEGER;
ALTER TABLE spelling_words ADD COLUMN vocabulary_difficulty_calculation_method TEXT;

-- Step 4: Add comments to document the new fields
COMMENT ON COLUMN spelling_words.vocabulary_difficulty_level IS 'Vocabulary difficulty level 1-5 (1=Foundation, 2=Academic, 3=Sophisticated, 4=Specialized, 5=Scholarly)';
COMMENT ON COLUMN spelling_words.vocabulary_difficulty_name IS 'Human-readable vocabulary difficulty name (Foundation, Academic, Sophisticated, Specialized, Scholarly)';
COMMENT ON COLUMN spelling_words.vocabulary_semantic_complexity_score IS 'Semantic complexity score 0-100 based on abstractness and conceptual depth';
COMMENT ON COLUMN spelling_words.vocabulary_contextual_frequency_score IS 'Contextual frequency score 0-100 based on usage in formal/academic contexts';
COMMENT ON COLUMN spelling_words.vocabulary_conceptual_sophistication_score IS 'Conceptual sophistication score 0-100 based on cognitive complexity required';
COMMENT ON COLUMN spelling_words.vocabulary_register_specificity_score IS 'Register specificity score 0-100 based on domain specificity';
COMMENT ON COLUMN spelling_words.vocabulary_difficulty_calculation_method IS 'Method used to calculate vocabulary difficulty (e.g., "Claude AI", "Manual", "API")';