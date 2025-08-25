-- Insert Spanish vocabulary into database
-- First create the schema, then insert sample data

-- ============================================================================
-- RUN THE SCHEMA CREATION FIRST (create_language_vocabulary_schema.sql)
-- ============================================================================

-- ============================================================================
-- INSERT SAMPLE SPANISH VOCABULARY
-- ============================================================================

-- Clear any existing Spanish vocabulary (for testing)
DELETE FROM language_vocabulary WHERE language = 'es';

-- Insert Basic level words (Zipf 5+)
INSERT INTO language_vocabulary (language, word, zipf_frequency, difficulty_id, english_translation, pronunciation_guide, part_of_speech, definition_english, translation_source) VALUES
('es', 'la', 7.6, 1, 'the', 'la', 'article', 'the (feminine singular)', 'GoogleTranslator'),
('es', 'que', 7.5, 1, 'that', 'keh', 'conjunction', 'that, which', 'GoogleTranslator'),
('es', 'los', 7.2, 1, 'the', 'los', 'article', 'the (masculine plural)', 'GoogleTranslator'),
('es', 'se', 7.1, 1, 'oneself', 'seh', 'pronoun', 'reflexive pronoun (himself/herself/itself)', 'GoogleTranslator'),
('es', 'las', 7.0, 1, 'the', 'las', 'article', 'the (feminine plural)', 'GoogleTranslator'),
('es', 'con', 7.0, 1, 'with', 'kon', 'preposition', 'with', 'GoogleTranslator'),
('es', 'una', 7.0, 1, 'a/one', 'oo-nah', 'article', 'a, an, one (feminine)', 'GoogleTranslator'),
('es', 'para', 6.9, 1, 'for', 'pah-rah', 'preposition', 'for, to, in order to', 'GoogleTranslator'),
('es', 'me', 6.7, 1, 'me', 'meh', 'pronoun', 'me (object pronoun)', 'GoogleTranslator'),
('es', 'pero', 6.6, 1, 'but', 'peh-roh', 'conjunction', 'but', 'GoogleTranslator');

-- Insert Elementary level words (Zipf 4.5-5)
INSERT INTO language_vocabulary (language, word, zipf_frequency, difficulty_id, english_translation, pronunciation_guide, part_of_speech, definition_english, translation_source) VALUES
('es', 'ciudad', 5.0, 2, 'city', 'see-oo-dahd', 'noun', 'city', 'GoogleTranslator'),
('es', 'clase', 5.0, 2, 'class', 'klah-seh', 'noun', 'class, lesson', 'GoogleTranslator'),
('es', 'colegio', 5.0, 2, 'school', 'koh-leh-hee-oh', 'noun', 'school (primary/secondary)', 'GoogleTranslator'),
('es', 'fiesta', 4.9, 2, 'party', 'fee-ehs-tah', 'noun', 'party, celebration', 'GoogleTranslator'),
('es', 'profesor', 4.8, 2, 'teacher', 'proh-feh-sohr', 'noun', 'teacher, professor', 'GoogleTranslator'),
('es', 'amigo', 4.8, 2, 'friend', 'ah-mee-goh', 'noun', 'friend (masculine)', 'GoogleTranslator'),
('es', 'familia', 4.7, 2, 'family', 'fah-mee-lee-ah', 'noun', 'family', 'GoogleTranslator'),
('es', 'trabajo', 4.7, 2, 'work', 'trah-bah-hoh', 'noun', 'work, job', 'GoogleTranslator'),
('es', 'escuela', 4.6, 2, 'school', 'ehs-kweh-lah', 'noun', 'school', 'GoogleTranslator'),
('es', 'estudiante', 4.5, 2, 'student', 'ehs-too-dee-ahn-teh', 'noun', 'student', 'GoogleTranslator');

-- Insert Intermediate level words (Zipf 4-4.5)
INSERT INTO language_vocabulary (language, word, zipf_frequency, difficulty_id, english_translation, pronunciation_guide, part_of_speech, definition_english, translation_source) VALUES
('es', 'abuelo', 4.5, 3, 'grandfather', 'ah-bweh-loh', 'noun', 'grandfather', 'GoogleTranslator'),
('es', 'computadora', 4.3, 3, 'computer', 'kohm-poo-tah-doh-rah', 'noun', 'computer', 'GoogleTranslator'),
('es', 'restaurante', 4.2, 3, 'restaurant', 'rehs-tow-rahn-teh', 'noun', 'restaurant', 'GoogleTranslator'),
('es', 'medicina', 4.2, 3, 'medicine', 'meh-dee-see-nah', 'noun', 'medicine', 'GoogleTranslator'),
('es', 'biblioteca', 4.1, 3, 'library', 'bee-blee-oh-teh-kah', 'noun', 'library', 'GoogleTranslator'),
('es', 'aeropuerto', 4.0, 3, 'airport', 'ah-eh-roh-pwehr-toh', 'noun', 'airport', 'GoogleTranslator'),
('es', 'apartamento', 4.0, 3, 'apartment', 'ah-pahr-tah-mehn-toh', 'noun', 'apartment', 'GoogleTranslator'),
('es', 'universidad', 4.0, 3, 'university', 'oo-nee-behr-see-dahd', 'noun', 'university', 'GoogleTranslator'),
('es', 'televisión', 4.0, 3, 'television', 'teh-leh-bee-see-ohn', 'noun', 'television', 'GoogleTranslator'),
('es', 'supermercado', 4.0, 3, 'supermarket', 'soo-pehr-mehr-kah-doh', 'noun', 'supermarket', 'GoogleTranslator');

-- Insert Advanced level words (Zipf 3.5-4)
INSERT INTO language_vocabulary (language, word, zipf_frequency, difficulty_id, english_translation, pronunciation_guide, part_of_speech, definition_english, translation_source) VALUES
('es', 'agradecimiento', 4.0, 4, 'gratitude', 'ah-grah-deh-see-mee-ehn-toh', 'noun', 'gratitude, thanks', 'GoogleTranslator'),
('es', 'cooperación', 3.9, 4, 'cooperation', 'koh-oh-peh-rah-see-ohn', 'noun', 'cooperation', 'GoogleTranslator'),
('es', 'democracia', 3.8, 4, 'democracy', 'deh-moh-krah-see-ah', 'noun', 'democracy', 'GoogleTranslator'),
('es', 'administración', 3.8, 4, 'administration', 'ahd-mee-nees-trah-see-ohn', 'noun', 'administration', 'GoogleTranslator'),
('es', 'investigación', 3.7, 4, 'research', 'een-behs-tee-gah-see-ohn', 'noun', 'research, investigation', 'GoogleTranslator'),
('es', 'arquitectura', 3.6, 4, 'architecture', 'ahr-kee-tehk-too-rah', 'noun', 'architecture', 'GoogleTranslator'),
('es', 'infraestructura', 3.5, 4, 'infrastructure', 'een-frah-ehs-trook-too-rah', 'noun', 'infrastructure', 'GoogleTranslator'),
('es', 'biodiversidad', 3.5, 4, 'biodiversity', 'bee-oh-dee-behr-see-dahd', 'noun', 'biodiversity', 'GoogleTranslator'),
('es', 'sostenibilidad', 3.5, 4, 'sustainability', 'sohs-teh-nee-bee-lee-dahd', 'noun', 'sustainability', 'GoogleTranslator'),
('es', 'globalización', 3.5, 4, 'globalization', 'gloh-bah-lee-sah-see-ohn', 'noun', 'globalization', 'GoogleTranslator');

-- Insert Expert level words (Zipf 3-3.5)
INSERT INTO language_vocabulary (language, word, zipf_frequency, difficulty_id, english_translation, pronunciation_guide, part_of_speech, definition_english, translation_source) VALUES
('es', 'epistemología', 3.2, 5, 'epistemology', 'eh-pees-teh-moh-loh-hee-ah', 'noun', 'epistemology (study of knowledge)', 'GoogleTranslator'),
('es', 'metamorfosis', 3.1, 5, 'metamorphosis', 'meh-tah-mohr-foh-sees', 'noun', 'metamorphosis', 'GoogleTranslator'),
('es', 'idiosincrasia', 3.0, 5, 'idiosyncrasy', 'ee-dee-oh-seen-krah-see-ah', 'noun', 'idiosyncrasy', 'GoogleTranslator'),
('es', 'paradigma', 3.3, 5, 'paradigm', 'pah-rah-deeg-mah', 'noun', 'paradigm', 'GoogleTranslator'),
('es', 'sinergia', 3.2, 5, 'synergy', 'see-nehr-hee-ah', 'noun', 'synergy', 'GoogleTranslator'),
('es', 'paradoja', 3.1, 5, 'paradox', 'pah-rah-doh-hah', 'noun', 'paradox', 'GoogleTranslator'),
('es', 'dicotomía', 3.0, 5, 'dichotomy', 'dee-koh-toh-mee-ah', 'noun', 'dichotomy', 'GoogleTranslator'),
('es', 'simbiosis', 3.0, 5, 'symbiosis', 'seem-bee-oh-sees', 'noun', 'symbiosis', 'GoogleTranslator'),
('es', 'heterogéneo', 3.0, 5, 'heterogeneous', 'eh-teh-roh-heh-neh-oh', 'adjective', 'heterogeneous', 'GoogleTranslator'),
('es', 'axioma', 3.0, 5, 'axiom', 'ahk-see-oh-mah', 'noun', 'axiom', 'GoogleTranslator');

-- ============================================================================
-- CREATE STUDY LISTS FOR SPANISH VOCABULARY
-- ============================================================================

-- Create study lists for each difficulty level
INSERT INTO language_vocabulary_study_lists (name, description, language, difficulty_id, min_zipf, max_zipf, is_public) VALUES
('Spanish Basic Vocabulary', 'Most common Spanish words (Zipf 5+)', 'es', 1, 5.0, NULL, true),
('Spanish Elementary Vocabulary', 'Common Spanish words (Zipf 4.5-5)', 'es', 2, 4.5, 5.0, true),
('Spanish Intermediate Vocabulary', 'Moderate frequency Spanish words (Zipf 4-4.5)', 'es', 3, 4.0, 4.5, true),
('Spanish Advanced Vocabulary', 'Less common Spanish words (Zipf 3.5-4)', 'es', 4, 3.5, 4.0, true),
('Spanish Expert Vocabulary', 'Rare Spanish words (Zipf 3-3.5)', 'es', 5, 3.0, 3.5, true);

-- ============================================================================
-- VERIFY INSERTION
-- ============================================================================

SELECT 'Spanish vocabulary insertion complete' as status;

-- Check counts by difficulty
SELECT 
    lvd.difficulty_name,
    COUNT(*) as word_count,
    MIN(lv.zipf_frequency) as min_zipf,
    MAX(lv.zipf_frequency) as max_zipf
FROM language_vocabulary lv
JOIN language_vocabulary_difficulties lvd ON lv.difficulty_id = lvd.id
WHERE lv.language = 'es'
GROUP BY lvd.difficulty_name, lvd.display_order
ORDER BY lvd.display_order;

-- Show sample words
SELECT 
    word,
    english_translation,
    pronunciation_guide,
    zipf_frequency,
    difficulty_id
FROM language_vocabulary
WHERE language = 'es'
ORDER BY zipf_frequency DESC
LIMIT 10;