-- Create foreign language vocabulary tables
-- This will store vocabulary for all languages with difficulty based on Zipf frequency

-- ============================================================================
-- STEP 1: CREATE VOCABULARY DIFFICULTY TABLE (Foreign Key)
-- ============================================================================

CREATE TABLE IF NOT EXISTS language_vocabulary_difficulties (
    id INTEGER PRIMARY KEY,
    difficulty_name VARCHAR(50) NOT NULL,
    min_zipf DECIMAL(3,1) NOT NULL,
    max_zipf DECIMAL(3,1),
    description TEXT,
    display_order INTEGER
);

-- Insert difficulty levels based on Zipf ranges
INSERT INTO language_vocabulary_difficulties (id, difficulty_name, min_zipf, max_zipf, description, display_order) VALUES
(1, 'Basic', 5.0, NULL, 'Most common words (Zipf 5+)', 1),
(2, 'Elementary', 4.5, 5.0, 'Common words (Zipf 4.5-5)', 2),
(3, 'Intermediate', 4.0, 4.5, 'Moderate frequency (Zipf 4-4.5)', 3),
(4, 'Advanced', 3.5, 4.0, 'Less common (Zipf 3.5-4)', 4),
(5, 'Expert', 3.0, 3.5, 'Rare words (Zipf 3-3.5)', 5);

-- ============================================================================
-- STEP 2: CREATE MAIN LANGUAGE VOCABULARY TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS language_vocabulary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language VARCHAR(10) NOT NULL, -- ISO language code (es, fr, de, etc.)
    word VARCHAR(100) NOT NULL,
    base_form VARCHAR(100), -- Root/infinitive form if this is a variation
    zipf_frequency DECIMAL(3,1) NOT NULL,
    difficulty_id INTEGER REFERENCES language_vocabulary_difficulties(id),
    english_translation VARCHAR(255),
    pronunciation_guide VARCHAR(255), -- Phonetic respelling
    ipa_pronunciation VARCHAR(255), -- IPA notation if available
    part_of_speech VARCHAR(50),
    definition_english TEXT,
    example_sentence TEXT,
    example_sentence_translation TEXT,
    memory_tips TEXT,
    cognate_note TEXT, -- Note if word is similar to English
    false_friend_warning TEXT, -- Warning if word looks similar but means different
    difficulty_source VARCHAR(100) DEFAULT 'wordfreq',
    word_source VARCHAR(100) DEFAULT 'wordfreq',
    translation_source VARCHAR(100),
    definition_source VARCHAR(100),
    example_source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(language, word)
);

-- Create indexes for performance
CREATE INDEX idx_language_vocabulary_language ON language_vocabulary(language);
CREATE INDEX idx_language_vocabulary_zipf ON language_vocabulary(zipf_frequency);
CREATE INDEX idx_language_vocabulary_difficulty ON language_vocabulary(difficulty_id);
CREATE INDEX idx_language_vocabulary_word ON language_vocabulary(word);
CREATE INDEX idx_language_vocabulary_base_form ON language_vocabulary(base_form);

-- ============================================================================
-- STEP 3: CREATE USER PROGRESS TRACKING TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS language_vocabulary_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    vocabulary_id UUID REFERENCES language_vocabulary(id) ON DELETE CASCADE,
    times_reviewed INTEGER DEFAULT 0,
    times_correct INTEGER DEFAULT 0,
    last_reviewed TIMESTAMP,
    next_review TIMESTAMP,
    ease_factor DECIMAL(3,2) DEFAULT 2.5,
    interval_days INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, vocabulary_id)
);

-- ============================================================================
-- STEP 4: CREATE STUDY LISTS FOR LANGUAGE VOCABULARY
-- ============================================================================

CREATE TABLE IF NOT EXISTS language_vocabulary_study_lists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    language VARCHAR(10) NOT NULL,
    difficulty_id INTEGER REFERENCES language_vocabulary_difficulties(id),
    min_zipf DECIMAL(3,1),
    max_zipf DECIMAL(3,1),
    is_public BOOLEAN DEFAULT true,
    created_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- STEP 5: CREATE JUNCTION TABLE FOR STUDY LIST ITEMS
-- ============================================================================

CREATE TABLE IF NOT EXISTS language_vocabulary_study_list_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    study_list_id UUID REFERENCES language_vocabulary_study_lists(id) ON DELETE CASCADE,
    vocabulary_id UUID REFERENCES language_vocabulary(id) ON DELETE CASCADE,
    display_order INTEGER,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(study_list_id, vocabulary_id)
);

-- ============================================================================
-- STEP 6: CREATE VIEW FOR EASIER QUERYING
-- ============================================================================

CREATE OR REPLACE VIEW language_vocabulary_with_difficulty AS
SELECT 
    lv.*,
    lvd.difficulty_name,
    lvd.description as difficulty_description,
    CASE 
        WHEN lv.cognate_note IS NOT NULL THEN true
        ELSE false
    END as is_cognate,
    CASE
        WHEN lv.false_friend_warning IS NOT NULL THEN true
        ELSE false
    END as is_false_friend
FROM language_vocabulary lv
LEFT JOIN language_vocabulary_difficulties lvd ON lv.difficulty_id = lvd.id;

-- ============================================================================
-- STEP 7: ENABLE ROW LEVEL SECURITY
-- ============================================================================

ALTER TABLE language_vocabulary_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own progress" ON language_vocabulary_progress
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own progress" ON language_vocabulary_progress
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own progress" ON language_vocabulary_progress
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own progress" ON language_vocabulary_progress
    FOR DELETE USING (auth.uid() = user_id);

-- Public vocabulary is viewable by all
ALTER TABLE language_vocabulary ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Language vocabulary is viewable by all" ON language_vocabulary
    FOR SELECT USING (true);

-- ============================================================================
-- SUMMARY
-- ============================================================================

SELECT 'Language vocabulary schema created successfully' as status;