-- Copy Henle Latin questions from questions table to language_questions table
-- This is needed because module_questions links to language_questions, not questions

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
    '84acf185-0b8c-4c2a-99f3-c5056be86d23' as language_id,  -- Latin language ID
    'ba82c8e3-6e4d-408b-8386-d96c745d216a' as category_id,  -- Use existing category ID
    q.question_text,
    'multiple_choice' as question_type,
    q.options,
    q.correct_answer as correct_answer_index,
    q.explanation,
    1 as difficulty_level  -- 1 = beginner
FROM questions q
WHERE 
    -- Latin-specific questions based on content
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
    OR q.question_text LIKE '%genitive%'
    OR q.question_text LIKE '%nominative%'
    OR q.question_text LIKE '%accusative%'
    OR q.question_text LIKE '%ablative%'
    OR q.question_text LIKE '%dative%'
    OR q.question_text LIKE '%equus%'
    OR q.question_text LIKE '%dōnum%'
    OR q.question_text LIKE '%verbum%'
    OR q.question_text LIKE '%oppidum%'
    OR q.question_text LIKE '%rēgnum%'
    OR q.question_text LIKE '%fīlius%'
    OR q.question_text LIKE '%deus%'
    OR q.question_text LIKE '%Dominus%'
    OR q.question_text LIKE '%Templa%'
    OR q.question_text LIKE '%Puellae%'
    OR q.question_text LIKE '%Est bonus%'
    OR q.question_text LIKE '%Nōs ___ amīcī%'
    OR q.question_text LIKE '%porta%'
    OR q.question_text LIKE '%rosam%'
    OR q.question_text LIKE '%fēminae%'
    OR q.question_text LIKE '%cantat%'
ON CONFLICT DO NOTHING;

-- Count how many were inserted
SELECT COUNT(*) as latin_questions_count
FROM language_questions 
WHERE language_id = '84acf185-0b8c-4c2a-99f3-c5056be86d23';