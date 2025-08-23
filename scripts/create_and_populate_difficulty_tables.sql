-- Create and populate difficulty lookup tables
-- These tables store the difficulty level definitions

-- Create vocabulary_difficulties table
CREATE TABLE IF NOT EXISTS vocabulary_difficulties (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    min_age INTEGER,
    max_age INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create spelling_difficulties table  
CREATE TABLE IF NOT EXISTS spelling_difficulties (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Populate vocabulary_difficulties
INSERT INTO vocabulary_difficulties (id, name, description, min_age, max_age) VALUES
(1, 'Elementary', 'Basic vocabulary for ages 6-10', 6, 10),
(2, 'Middle School', 'Intermediate vocabulary for ages 11-13', 11, 13),
(3, 'High School', 'Advanced vocabulary for ages 14-17', 14, 17),
(4, 'College', 'College-level vocabulary for ages 18+', 18, 25),
(5, 'Advanced', 'Graduate level and specialized vocabulary', 22, NULL)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    min_age = EXCLUDED.min_age,
    max_age = EXCLUDED.max_age;

-- Populate spelling_difficulties
INSERT INTO spelling_difficulties (id, name, description) VALUES
(1, 'Easy', 'Common phonetic patterns, regular spelling'),
(2, 'Medium', 'Some irregular patterns, silent letters'),
(3, 'Hard', 'Complex or irregular spelling, multiple syllables'),
(4, 'Expert', 'Very challenging spelling, uncommon patterns')
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description;

-- Add foreign key constraints if they don't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'spelling_words_vocabulary_difficulty_id_fkey'
        AND table_name = 'spelling_words'
    ) THEN
        ALTER TABLE spelling_words 
        ADD CONSTRAINT spelling_words_vocabulary_difficulty_id_fkey 
        FOREIGN KEY (vocabulary_difficulty_id) 
        REFERENCES vocabulary_difficulties(id);
    END IF;
    
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'spelling_words_spelling_difficulty_id_fkey'
        AND table_name = 'spelling_words'
    ) THEN
        ALTER TABLE spelling_words 
        ADD CONSTRAINT spelling_words_spelling_difficulty_id_fkey 
        FOREIGN KEY (spelling_difficulty_id) 
        REFERENCES spelling_difficulties(id);
    END IF;
END $$;

-- Verify the tables and data
SELECT 'Vocabulary Difficulties:' as info;
SELECT * FROM vocabulary_difficulties ORDER BY id;

SELECT 'Spelling Difficulties:' as info;
SELECT * FROM spelling_difficulties ORDER BY id;

SELECT 'Distribution of words by difficulty:' as info;
SELECT 
    vd.name as vocabulary_level,
    sd.name as spelling_level,
    COUNT(*) as word_count
FROM spelling_words sw
LEFT JOIN vocabulary_difficulties vd ON sw.vocabulary_difficulty_id = vd.id
LEFT JOIN spelling_difficulties sd ON sw.spelling_difficulty_id = sd.id
GROUP BY vd.name, sd.name, vd.id, sd.id
ORDER BY vd.id, sd.id;