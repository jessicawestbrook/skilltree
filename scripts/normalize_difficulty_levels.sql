-- Normalize spelling and vocabulary difficulty levels into foreign key tables
-- This migration creates lookup tables for difficulty levels and updates the spelling_words table

-- Step 1: Create backup table
CREATE TABLE IF NOT EXISTS spelling_words_bkp3 AS SELECT * FROM spelling_words;

-- Step 2: Create spelling difficulty levels table
CREATE TABLE IF NOT EXISTS spelling_difficulty_levels (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  grade_equivalent TEXT,
  characteristics TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Step 3: Create vocabulary difficulty levels table  
CREATE TABLE IF NOT EXISTS vocabulary_difficulty_levels (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  characteristics TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Step 4: Populate spelling difficulty levels based on THEORETICAL_FOUNDATIONS.md
INSERT INTO spelling_difficulty_levels (id, name, description, grade_equivalent, characteristics) VALUES
(1, 'Beginner', 'Common everyday vocabulary, phonetic spelling, basic patterns', 'Grades 1-3', 'friend, because, special'),
(2, 'Elementary', 'Standard school vocabulary, introduction to silent letters, common prefixes/suffixes', 'Grades 4-5', 'beautiful, knowledge, necessary'),
(3, 'Intermediate', 'Complex patterns, foreign borrowings, multiple syllables, irregular spellings', 'Grades 6-8', 'rhythm, conscience, restaurant'),
(4, 'Advanced', 'Etymology-based spelling, uncommon letter combinations, technical vocabulary', 'Grades 9-12 (Regional)', 'pharaoh, silhouette, entrepreneur'),
(5, 'Expert', 'Championship words, rare etymology, complex linguistic origins', 'Competition Level', 'pneumonia, onomatopoeia, schadenfreude')
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  grade_equivalent = EXCLUDED.grade_equivalent,
  characteristics = EXCLUDED.characteristics,
  updated_at = NOW();

-- Step 5: Populate vocabulary difficulty levels based on THEORETICAL_FOUNDATIONS.md
INSERT INTO vocabulary_difficulty_levels (id, name, description, characteristics) VALUES
(1, 'Foundation', 'Basic everyday concepts', 'Concrete nouns, simple actions, common adjectives - happy, run, big, house, dog'),
(2, 'Academic', 'School-level vocabulary', 'Abstract concepts, academic subjects, formal language - analyze, democracy, ecosystem, literature'),
(3, 'Sophisticated', 'Advanced academic and professional', 'Complex abstractions, technical concepts, nuanced meanings - paradigm, synthesize, empirical, rhetoric'),
(4, 'Specialized', 'Domain-specific terminology', 'Professional jargon, scientific terms, specialized fields - cytoplasm, jurisprudence, thermodynamics, epistemology'),
(5, 'Scholarly', 'Research and expert-level', 'Highly specialized, theoretical concepts, academic discourse - phenomenology, hermeneutics, ontological, epistemic')
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  characteristics = EXCLUDED.characteristics,
  updated_at = NOW();

-- Step 6: Add foreign key columns to spelling_words table
ALTER TABLE spelling_words ADD COLUMN spelling_difficulty_id INTEGER;
ALTER TABLE spelling_words ADD COLUMN vocabulary_difficulty_id INTEGER;

-- Step 7: Populate the foreign key columns based on existing data
UPDATE spelling_words 
SET spelling_difficulty_id = spelling_difficulty_level
WHERE spelling_difficulty_level IS NOT NULL;

UPDATE spelling_words 
SET vocabulary_difficulty_id = vocabulary_difficulty_level
WHERE vocabulary_difficulty_level IS NOT NULL;

-- Step 8: Add foreign key constraints
ALTER TABLE spelling_words 
ADD CONSTRAINT fk_spelling_difficulty 
FOREIGN KEY (spelling_difficulty_id) 
REFERENCES spelling_difficulty_levels(id);

ALTER TABLE spelling_words 
ADD CONSTRAINT fk_vocabulary_difficulty 
FOREIGN KEY (vocabulary_difficulty_id) 
REFERENCES vocabulary_difficulty_levels(id);

-- Step 9: Add comments
COMMENT ON TABLE spelling_difficulty_levels IS 'Lookup table for spelling difficulty levels based on orthographic complexity';
COMMENT ON TABLE vocabulary_difficulty_levels IS 'Lookup table for vocabulary difficulty levels based on semantic and conceptual complexity';
COMMENT ON COLUMN spelling_words.spelling_difficulty_id IS 'Foreign key to spelling_difficulty_levels table';
COMMENT ON COLUMN spelling_words.vocabulary_difficulty_id IS 'Foreign key to vocabulary_difficulty_levels table';

-- Step 10: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_spelling_words_spelling_difficulty_id ON spelling_words(spelling_difficulty_id);
CREATE INDEX IF NOT EXISTS idx_spelling_words_vocabulary_difficulty_id ON spelling_words(vocabulary_difficulty_id);

-- Verification queries (commented out - uncomment to run manually)
-- SELECT 'Spelling Difficulty Levels' as table_name, COUNT(*) as count FROM spelling_difficulty_levels
-- UNION ALL
-- SELECT 'Vocabulary Difficulty Levels' as table_name, COUNT(*) as count FROM vocabulary_difficulty_levels
-- UNION ALL  
-- SELECT 'Words with Spelling Difficulty FK' as table_name, COUNT(*) as count FROM spelling_words WHERE spelling_difficulty_id IS NOT NULL
-- UNION ALL
-- SELECT 'Words with Vocabulary Difficulty FK' as table_name, COUNT(*) as count FROM spelling_words WHERE vocabulary_difficulty_id IS NOT NULL;