-- Add conditional follow-up questions to the interests quiz
-- These questions appear based on answers to previous questions

-- ================================================
-- 1. Add conditional question fields to schema
-- ================================================
ALTER TABLE public.interests_quiz_questions
ADD COLUMN IF NOT EXISTS parent_question_id UUID REFERENCES public.interests_quiz_questions(id),
ADD COLUMN IF NOT EXISTS condition_type TEXT CHECK (condition_type IN ('contains', 'equals', 'greater_than', 'selected')),
ADD COLUMN IF NOT EXISTS condition_value JSONB,
ADD COLUMN IF NOT EXISTS is_follow_up BOOLEAN DEFAULT false;

-- Create index for follow-up questions
CREATE INDEX IF NOT EXISTS idx_quiz_questions_parent 
ON public.interests_quiz_questions(parent_question_id, is_active);

-- ================================================
-- 2. Update existing questions to mark them as primary
-- ================================================
UPDATE public.interests_quiz_questions
SET is_follow_up = false
WHERE parent_question_id IS NULL;

-- ================================================
-- 3. Add follow-up questions for specific interests
-- ================================================

-- Get IDs of parent questions
DO $$
DECLARE
  subjects_question_id UUID;
  programming_question_id UUID;
  languages_question_id UUID;
  career_question_id UUID;
  learning_style_id UUID;
BEGIN
  -- Get the main questions IDs
  SELECT id INTO subjects_question_id FROM public.interests_quiz_questions 
  WHERE question_text = 'Which subjects interest you the most?' LIMIT 1;
  
  SELECT id INTO programming_question_id FROM public.interests_quiz_questions 
  WHERE question_text = 'How interested are you in learning programming?' LIMIT 1;
  
  SELECT id INTO languages_question_id FROM public.interests_quiz_questions 
  WHERE question_text = 'Which languages would you like to learn?' LIMIT 1;
  
  SELECT id INTO career_question_id FROM public.interests_quiz_questions 
  WHERE question_text = 'Which career fields interest you?' LIMIT 1;
  
  SELECT id INTO learning_style_id FROM public.interests_quiz_questions 
  WHERE question_text = 'What is your preferred learning style?' LIMIT 1;

  -- ================================================
  -- Follow-ups for MATHEMATICS interest
  -- ================================================
  INSERT INTO public.interests_quiz_questions (
    question_text, question_type, category, options, display_order,
    parent_question_id, condition_type, condition_value, is_follow_up
  ) VALUES 
  (
    'Which areas of mathematics interest you most?',
    'multi_select',
    'mathematics',
    '["Algebra", "Geometry", "Calculus", "Statistics", "Number Theory", "Applied Mathematics", "Discrete Mathematics", "Linear Algebra", "Probability", "Mathematical Logic"]'::jsonb,
    101,
    subjects_question_id,
    'contains',
    '"Mathematics"'::jsonb,
    true
  ),
  (
    'What is your current math level?',
    'multiple_choice',
    'mathematics',
    '["Elementary (Basic Arithmetic)", "Pre-Algebra", "Algebra I", "Geometry", "Algebra II", "Pre-Calculus", "Calculus", "Advanced College Mathematics", "Graduate Level"]'::jsonb,
    102,
    subjects_question_id,
    'contains',
    '"Mathematics"'::jsonb,
    true
  );

  -- ================================================
  -- Follow-ups for SCIENCE interest
  -- ================================================
  INSERT INTO public.interests_quiz_questions (
    question_text, question_type, category, options, display_order,
    parent_question_id, condition_type, condition_value, is_follow_up
  ) VALUES 
  (
    'Which sciences are you most interested in?',
    'multi_select',
    'science',
    '["Physics", "Chemistry", "Biology", "Earth Science", "Astronomy", "Environmental Science", "Computer Science", "Neuroscience", "Psychology", "Engineering"]'::jsonb,
    103,
    subjects_question_id,
    'contains',
    '"Science"'::jsonb,
    true
  ),
  (
    'What aspect of science interests you most?',
    'multiple_choice',
    'science',
    '["Conducting experiments", "Understanding theories", "Solving real-world problems", "Research and discovery", "Technology applications", "Medical applications", "Environmental impact"]'::jsonb,
    104,
    subjects_question_id,
    'contains',
    '"Science"'::jsonb,
    true
  );

  -- ================================================
  -- Follow-ups for PROGRAMMING interest (scale >= 3)
  -- ================================================
  INSERT INTO public.interests_quiz_questions (
    question_text, question_type, category, options, display_order,
    parent_question_id, condition_type, condition_value, is_follow_up
  ) VALUES 
  (
    'Which programming languages would you like to learn?',
    'multi_select',
    'programming',
    '["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "SQL", "R", "MATLAB"]'::jsonb,
    105,
    programming_question_id,
    'greater_than',
    '2'::jsonb,
    true
  ),
  (
    'What do you want to build with programming?',
    'multi_select',
    'programming',
    '["Websites", "Mobile Apps", "Games", "Data Analysis Tools", "AI/Machine Learning", "Automation Scripts", "Desktop Applications", "IoT/Embedded Systems", "Blockchain/Crypto", "APIs/Backend Services"]'::jsonb,
    106,
    programming_question_id,
    'greater_than',
    '2'::jsonb,
    true
  ),
  (
    'What is your current programming experience?',
    'multiple_choice',
    'programming',
    '["Complete beginner", "I''ve tried some tutorials", "I can write simple programs", "I''m comfortable with basics", "I''m intermediate level", "I''m advanced"]'::jsonb,
    107,
    programming_question_id,
    'greater_than',
    '2'::jsonb,
    true
  );

  -- ================================================
  -- Follow-ups for LANGUAGE learning
  -- ================================================
  INSERT INTO public.interests_quiz_questions (
    question_text, question_type, category, options, display_order,
    parent_question_id, condition_type, condition_value, is_follow_up
  ) VALUES 
  (
    'For Spanish: What is your current level?',
    'multiple_choice',
    'languages',
    '["Complete beginner", "Know some words", "Basic conversations", "Intermediate", "Advanced", "Near fluent"]'::jsonb,
    108,
    languages_question_id,
    'contains',
    '"Spanish"'::jsonb,
    true
  ),
  (
    'For Spanish: What aspects would you like to focus on?',
    'multi_select',
    'languages',
    '["Speaking/Conversation", "Grammar", "Vocabulary", "Reading", "Writing", "Listening", "Business Spanish", "Travel Spanish", "Cultural knowledge"]'::jsonb,
    109,
    languages_question_id,
    'contains',
    '"Spanish"'::jsonb,
    true
  ),
  (
    'For French: What is your current level?',
    'multiple_choice',
    'languages',
    '["Complete beginner", "Know some words", "Basic conversations", "Intermediate", "Advanced", "Near fluent"]'::jsonb,
    110,
    languages_question_id,
    'contains',
    '"French"'::jsonb,
    true
  ),
  (
    'For Chinese: Which variety would you like to learn?',
    'multiple_choice',
    'languages',
    '["Mandarin (Simplified)", "Mandarin (Traditional)", "Cantonese", "Both Mandarin and Cantonese", "Not sure yet"]'::jsonb,
    111,
    languages_question_id,
    'contains',
    '"Chinese"'::jsonb,
    true
  );

  -- ================================================
  -- Follow-ups for HISTORY interest
  -- ================================================
  INSERT INTO public.interests_quiz_questions (
    question_text, question_type, category, options, display_order,
    parent_question_id, condition_type, condition_value, is_follow_up
  ) VALUES 
  (
    'Which historical periods interest you most?',
    'multi_select',
    'history',
    '["Ancient History", "Medieval Period", "Renaissance", "Age of Exploration", "Industrial Revolution", "World War I", "World War II", "Cold War", "Modern History", "Prehistory"]'::jsonb,
    112,
    subjects_question_id,
    'contains',
    '"History"'::jsonb,
    true
  ),
  (
    'Which regions'' history interests you most?',
    'multi_select',
    'history',
    '["United States", "Europe", "Asia", "Middle East", "Africa", "Latin America", "Ancient Civilizations", "World History", "Local/Regional History"]'::jsonb,
    113,
    subjects_question_id,
    'contains',
    '"History"'::jsonb,
    true
  );

  -- ================================================
  -- Follow-ups for TECHNOLOGY career interest
  -- ================================================
  INSERT INTO public.interests_quiz_questions (
    question_text, question_type, category, options, display_order,
    parent_question_id, condition_type, condition_value, is_follow_up
  ) VALUES 
  (
    'Which technology careers interest you most?',
    'multi_select',
    'career',
    '["Software Developer", "Data Scientist", "Cybersecurity", "Web Developer", "Mobile Developer", "Cloud Engineer", "AI/ML Engineer", "DevOps", "UX/UI Designer", "IT Support", "Database Administrator", "Game Developer"]'::jsonb,
    114,
    career_question_id,
    'contains',
    '"Technology"'::jsonb,
    true
  ),
  (
    'What technical skills would you like to develop?',
    'multi_select',
    'career',
    '["Programming", "Data Analysis", "Cloud Computing", "Networking", "Security", "Databases", "Web Technologies", "Mobile Development", "AI/Machine Learning", "System Administration"]'::jsonb,
    115,
    career_question_id,
    'contains',
    '"Technology"'::jsonb,
    true
  );

  -- ================================================
  -- Follow-ups for CREATIVE/ARTS interest
  -- ================================================
  INSERT INTO public.interests_quiz_questions (
    question_text, question_type, category, options, display_order,
    parent_question_id, condition_type, condition_value, is_follow_up
  ) VALUES 
  (
    'Which creative fields interest you?',
    'multi_select',
    'creative',
    '["Visual Arts/Painting", "Digital Art", "Music Composition", "Music Performance", "Creative Writing", "Film/Video", "Photography", "Graphic Design", "Animation", "Theater/Drama", "Dance", "Fashion Design"]'::jsonb,
    116,
    career_question_id,
    'contains',
    '"Creative/Arts"'::jsonb,
    true
  ),
  (
    'What is your experience level in creative arts?',
    'multiple_choice',
    'creative',
    '["Complete beginner", "Hobbyist", "Some formal training", "Intermediate", "Advanced", "Professional"]'::jsonb,
    117,
    career_question_id,
    'contains',
    '"Creative/Arts"'::jsonb,
    true
  );

  -- ================================================
  -- Follow-ups for HEALTHCARE interest
  -- ================================================
  INSERT INTO public.interests_quiz_questions (
    question_text, question_type, category, options, display_order,
    parent_question_id, condition_type, condition_value, is_follow_up
  ) VALUES 
  (
    'Which healthcare areas interest you most?',
    'multi_select',
    'healthcare',
    '["Medicine/Doctor", "Nursing", "Mental Health", "Physical Therapy", "Pharmacy", "Medical Research", "Public Health", "Nutrition", "Medical Technology", "Healthcare Administration", "Veterinary Medicine"]'::jsonb,
    118,
    career_question_id,
    'contains',
    '"Healthcare"'::jsonb,
    true
  );

  -- ================================================
  -- Follow-ups for VISUAL learning style
  -- ================================================
  INSERT INTO public.interests_quiz_questions (
    question_text, question_type, category, options, display_order,
    parent_question_id, condition_type, condition_value, is_follow_up
  ) VALUES 
  (
    'Which visual learning tools do you prefer?',
    'multi_select',
    'learning_preference',
    '["Infographics", "Mind Maps", "Video Tutorials", "Diagrams and Charts", "Interactive Simulations", "Slide Presentations", "Illustrated Books", "Flashcards with Images", "3D Models", "Animations"]'::jsonb,
    119,
    learning_style_id,
    'contains',
    '"Visual"'::jsonb,
    true
  );

END $$;

-- ================================================
-- 4. Create function to get follow-up questions
-- ================================================
CREATE OR REPLACE FUNCTION get_follow_up_questions(
  p_parent_id UUID,
  p_answer_value TEXT
) RETURNS TABLE (
  id UUID,
  question_text TEXT,
  question_type TEXT,
  category TEXT,
  options JSONB,
  display_order INTEGER
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    q.id,
    q.question_text,
    q.question_type,
    q.category,
    q.options,
    q.display_order
  FROM public.interests_quiz_questions q
  WHERE q.parent_question_id = p_parent_id
    AND q.is_active = true
    AND q.is_follow_up = true
    AND (
      -- Check condition based on type
      CASE 
        WHEN q.condition_type = 'contains' THEN
          p_answer_value::jsonb @> q.condition_value
        WHEN q.condition_type = 'equals' THEN
          p_answer_value = q.condition_value::text
        WHEN q.condition_type = 'greater_than' THEN
          p_answer_value::numeric > (q.condition_value::text)::numeric
        WHEN q.condition_type = 'selected' THEN
          p_answer_value IS NOT NULL AND p_answer_value != ''
        ELSE
          false
      END
    )
  ORDER BY q.display_order;
END;
$$ LANGUAGE plpgsql;

-- ================================================
-- 5. Create view for quiz flow
-- ================================================
CREATE OR REPLACE VIEW quiz_question_flow AS
SELECT 
  q.id,
  q.question_text,
  q.question_type,
  q.category,
  q.display_order,
  q.is_follow_up,
  p.question_text as parent_question,
  q.condition_type,
  q.condition_value
FROM public.interests_quiz_questions q
LEFT JOIN public.interests_quiz_questions p ON q.parent_question_id = p.id
WHERE q.is_active = true
ORDER BY q.display_order;

-- ================================================
-- 6. Grant permissions
-- ================================================
GRANT EXECUTE ON FUNCTION get_follow_up_questions(UUID, TEXT) TO authenticated;
GRANT SELECT ON quiz_question_flow TO authenticated;

-- ================================================
-- SUCCESS MESSAGE
-- ================================================
DO $$
DECLARE
  follow_up_count INTEGER;
  primary_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO follow_up_count 
  FROM public.interests_quiz_questions 
  WHERE is_follow_up = true;
  
  SELECT COUNT(*) INTO primary_count 
  FROM public.interests_quiz_questions 
  WHERE is_follow_up = false OR is_follow_up IS NULL;
  
  RAISE NOTICE '';
  RAISE NOTICE '========================================';
  RAISE NOTICE '✅ CONDITIONAL QUESTIONS ADDED';
  RAISE NOTICE '========================================';
  RAISE NOTICE '';
  RAISE NOTICE 'Question Statistics:';
  RAISE NOTICE '  Primary questions: %', primary_count;
  RAISE NOTICE '  Follow-up questions: %', follow_up_count;
  RAISE NOTICE '  Total questions: %', primary_count + follow_up_count;
  RAISE NOTICE '';
  RAISE NOTICE 'Follow-up categories added:';
  RAISE NOTICE '  • Mathematics (specific areas & level)';
  RAISE NOTICE '  • Science (specific fields & interests)';
  RAISE NOTICE '  • Programming (languages & projects)';
  RAISE NOTICE '  • Languages (levels & focus areas)';
  RAISE NOTICE '  • History (periods & regions)';
  RAISE NOTICE '  • Technology careers (roles & skills)';
  RAISE NOTICE '  • Creative arts (fields & experience)';
  RAISE NOTICE '  • Healthcare (specialties)';
  RAISE NOTICE '  • Learning preferences (tools)';
  RAISE NOTICE '';
  RAISE NOTICE 'The quiz now dynamically adapts based on user interests!';
  RAISE NOTICE '========================================';
END $$;