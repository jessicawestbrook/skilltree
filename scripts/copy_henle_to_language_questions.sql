-- Copy Henle Latin questions from questions table to language_questions table
-- This is needed because module_questions links to language_questions, not questions

-- Get Latin language ID
DO $$
DECLARE
    latin_lang_id UUID;
    grammar_cat_id UUID;
BEGIN
    -- Get Latin language ID
    SELECT id INTO latin_lang_id FROM languages WHERE name = 'Latin' LIMIT 1;
    
    -- Get or create Grammar category
    SELECT id INTO grammar_cat_id FROM question_categories WHERE name = 'Grammar' LIMIT 1;
    
    IF grammar_cat_id IS NULL THEN
        INSERT INTO question_categories (id, name, description)
        VALUES (gen_random_uuid(), 'Grammar', 'Grammar and syntax questions')
        RETURNING id INTO grammar_cat_id;
    END IF;
    
    -- Insert questions into language_questions
    INSERT INTO language_questions (
        id,
        language_id,
        category_id,
        question_text,
        question_type,
        options,
        correct_answer_index,
        explanation,
        difficulty_level
    )
    SELECT 
        gen_random_uuid() as id,
        latin_lang_id as language_id,
        grammar_cat_id as category_id,
        q.question_text,
        'multiple_choice' as question_type,
        q.options,
        q.correct_answer as correct_answer_index,
        q.explanation,
        CASE 
            WHEN q.difficulty = 'easy' THEN 'beginner'
            WHEN q.difficulty = 'average' THEN 'intermediate'
            WHEN q.difficulty = 'hard' THEN 'advanced'
            ELSE 'beginner'
        END as difficulty_level
    FROM questions q
    WHERE 
        q.question_text LIKE '%declension%' 
        OR q.question_text LIKE '%conjugation%'
        OR q.question_text LIKE '%Latin%'
        OR q.question_text LIKE '%puella%'
        OR q.question_text LIKE '%servus%'
        OR q.question_text LIKE '%amīcus%'
        OR q.question_text LIKE '%bellum%'
        OR q.question_text LIKE '%sum%'
        OR q.question_text LIKE '%amō%'
        OR q.question_text LIKE '%portō%'
        OR q.question_text LIKE '%vocās%'
        OR q.question_text LIKE '%laborant%'
        OR q.question_text LIKE '%laudō%'
    ON CONFLICT DO NOTHING;
    
    RAISE NOTICE 'Latin questions copied to language_questions table';
END $$;

-- Verify the copy
SELECT COUNT(*) as count, 'Total Latin questions' as description
FROM language_questions 
WHERE language_id = (SELECT id FROM languages WHERE name = 'Latin' LIMIT 1);