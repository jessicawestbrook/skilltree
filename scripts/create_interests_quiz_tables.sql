-- Create proper schema for interests quiz with row-based storage
-- This allows questions to change over time without altering the schema

-- ================================================
-- 1. Create quiz questions table
-- ================================================
CREATE TABLE IF NOT EXISTS public.interests_quiz_questions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  question_text TEXT NOT NULL,
  question_type TEXT NOT NULL CHECK (question_type IN ('multiple_choice', 'scale', 'text', 'multi_select')),
  category TEXT, -- e.g., 'academic', 'creative', 'technical', 'social'
  options JSONB, -- For multiple choice options
  display_order INTEGER,
  is_active BOOLEAN DEFAULT true,
  version INTEGER DEFAULT 1, -- Track question versions
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for active questions
CREATE INDEX IF NOT EXISTS idx_interests_quiz_questions_active 
ON public.interests_quiz_questions(is_active, display_order);

-- ================================================
-- 2. Create quiz responses table (main responses)
-- ================================================
CREATE TABLE IF NOT EXISTS public.interests_quiz_responses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  quiz_version INTEGER DEFAULT 1, -- Track which version of quiz was taken
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  is_complete BOOLEAN DEFAULT false,
  metadata JSONB, -- Store any additional context
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for user responses
CREATE INDEX IF NOT EXISTS idx_interests_quiz_responses_user 
ON public.interests_quiz_responses(user_id, completed_at DESC);

-- ================================================
-- 3. Create individual answer storage (row-based)
-- ================================================
CREATE TABLE IF NOT EXISTS public.interests_quiz_answers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  response_id UUID NOT NULL REFERENCES public.interests_quiz_responses(id) ON DELETE CASCADE,
  question_id UUID NOT NULL REFERENCES public.interests_quiz_questions(id),
  answer_value TEXT, -- Store answer as text, can be parsed based on question_type
  answer_metadata JSONB, -- Additional data like confidence, time_spent, etc.
  answered_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Ensure one answer per question per response
  UNIQUE(response_id, question_id)
);

-- Create composite index for efficient querying
CREATE INDEX IF NOT EXISTS idx_interests_quiz_answers_response 
ON public.interests_quiz_answers(response_id, question_id);

-- ================================================
-- 4. Create derived interests table (computed from answers)
-- ================================================
CREATE TABLE IF NOT EXISTS public.user_interests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  interest_category TEXT NOT NULL, -- e.g., 'mathematics', 'languages', 'science'
  interest_level DECIMAL(3,2) CHECK (interest_level >= 0 AND interest_level <= 1), -- 0-1 scale
  confidence_score DECIMAL(3,2), -- How confident we are in this interest
  source TEXT DEFAULT 'quiz', -- 'quiz', 'behavior', 'explicit', etc.
  quiz_response_id UUID REFERENCES public.interests_quiz_responses(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Allow multiple sources but track the latest per category
  UNIQUE(user_id, interest_category, source)
);

-- Create index for user interests lookup
CREATE INDEX IF NOT EXISTS idx_user_interests_user 
ON public.user_interests(user_id, interest_level DESC);

-- ================================================
-- 5. Add RLS policies
-- ================================================

-- Enable RLS on all tables
ALTER TABLE public.interests_quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.interests_quiz_responses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.interests_quiz_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_interests ENABLE ROW LEVEL SECURITY;

-- Quiz questions are viewable by everyone
CREATE POLICY "Quiz questions are viewable by everyone"
  ON public.interests_quiz_questions FOR SELECT
  USING (true);

-- Users can only manage their own responses
CREATE POLICY "Users can view own quiz responses"
  ON public.interests_quiz_responses FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own quiz responses"
  ON public.interests_quiz_responses FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own quiz responses"
  ON public.interests_quiz_responses FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can only manage their own answers
CREATE POLICY "Users can view own quiz answers"
  ON public.interests_quiz_answers FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.interests_quiz_responses r
      WHERE r.id = response_id AND r.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert own quiz answers"
  ON public.interests_quiz_answers FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.interests_quiz_responses r
      WHERE r.id = response_id AND r.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update own quiz answers"
  ON public.interests_quiz_answers FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM public.interests_quiz_responses r
      WHERE r.id = response_id AND r.user_id = auth.uid()
    )
  );

-- Users can only manage their own interests
CREATE POLICY "Users can view own interests"
  ON public.user_interests FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own interests"
  ON public.user_interests FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own interests"
  ON public.user_interests FOR UPDATE
  USING (auth.uid() = user_id);

-- ================================================
-- 6. Add some initial quiz questions
-- ================================================
INSERT INTO public.interests_quiz_questions (question_text, question_type, category, options, display_order)
VALUES 
  ('Which subjects interest you the most?', 'multi_select', 'academic', 
   '["Mathematics", "Science", "History", "Literature", "Languages", "Art", "Music", "Technology", "Business", "Psychology"]'::jsonb, 1),
  
  ('How interested are you in learning programming?', 'scale', 'technical',
   '{"min": 1, "max": 5, "labels": ["Not at all", "Slightly", "Moderately", "Very", "Extremely"]}'::jsonb, 2),
  
  ('What is your primary learning goal?', 'multiple_choice', 'goals',
   '["Career advancement", "Personal enrichment", "Academic success", "Skill development", "Hobby exploration"]'::jsonb, 3),
  
  ('Which languages would you like to learn?', 'multi_select', 'languages',
   '["Spanish", "French", "German", "Chinese", "Japanese", "Arabic", "Russian", "Italian", "Portuguese", "Korean"]'::jsonb, 4),
  
  ('How much time can you dedicate to learning per week?', 'multiple_choice', 'commitment',
   '["Less than 1 hour", "1-3 hours", "3-5 hours", "5-10 hours", "More than 10 hours"]'::jsonb, 5),
  
  ('What is your preferred learning style?', 'multiple_choice', 'style',
   '["Visual (videos, diagrams)", "Reading/Writing", "Hands-on practice", "Audio (podcasts, lectures)", "Interactive discussions"]'::jsonb, 6),
  
  ('Which career fields interest you?', 'multi_select', 'career',
   '["Healthcare", "Education", "Technology", "Business/Finance", "Creative/Arts", "Science/Research", "Engineering", "Law", "Public Service", "Trades/Crafts"]'::jsonb, 7),
  
  ('What is your current education level?', 'multiple_choice', 'background',
   '["Elementary School", "Middle School", "High School", "Some College", "Bachelor''s Degree", "Master''s Degree", "Doctorate", "Professional Certification"]'::jsonb, 8),
  
  ('How comfortable are you with technology?', 'scale', 'technical',
   '{"min": 1, "max": 5, "labels": ["Beginner", "Basic", "Intermediate", "Advanced", "Expert"]}'::jsonb, 9),
  
  ('What motivates you to learn?', 'multi_select', 'motivation',
   '["Career growth", "Personal satisfaction", "Social recognition", "Financial rewards", "Intellectual curiosity", "Problem solving", "Helping others", "Creative expression"]'::jsonb, 10)
ON CONFLICT DO NOTHING;

-- ================================================
-- 7. Create function to compute interests from quiz
-- ================================================
CREATE OR REPLACE FUNCTION compute_user_interests(p_response_id UUID)
RETURNS void AS $$
DECLARE
  v_user_id UUID;
  v_interest RECORD;
BEGIN
  -- Get user_id from response
  SELECT user_id INTO v_user_id
  FROM public.interests_quiz_responses
  WHERE id = p_response_id;
  
  -- Clear previous quiz-based interests for this user
  DELETE FROM public.user_interests
  WHERE user_id = v_user_id AND source = 'quiz';
  
  -- Compute interests based on answers
  -- This is a simplified example - you can make this more sophisticated
  FOR v_interest IN
    SELECT 
      q.category as interest_category,
      AVG(
        CASE 
          WHEN q.question_type = 'scale' THEN 
            (a.answer_value::numeric - 1) / 4.0  -- Convert 1-5 scale to 0-1
          WHEN a.answer_value IS NOT NULL THEN 
            0.8  -- Default high interest if answered
          ELSE 
            0.2  -- Low interest if not answered
        END
      ) as interest_level
    FROM public.interests_quiz_questions q
    LEFT JOIN public.interests_quiz_answers a 
      ON a.question_id = q.id AND a.response_id = p_response_id
    WHERE q.category IS NOT NULL
    GROUP BY q.category
  LOOP
    INSERT INTO public.user_interests (
      user_id, 
      interest_category, 
      interest_level, 
      confidence_score,
      source,
      quiz_response_id
    ) VALUES (
      v_user_id,
      v_interest.interest_category,
      v_interest.interest_level,
      0.7, -- Default confidence
      'quiz',
      p_response_id
    );
  END LOOP;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ================================================
-- 8. Create trigger to compute interests on quiz completion
-- ================================================
CREATE OR REPLACE FUNCTION trigger_compute_interests()
RETURNS trigger AS $$
BEGIN
  IF NEW.is_complete = true AND OLD.is_complete = false THEN
    PERFORM compute_user_interests(NEW.id);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_quiz_complete
  AFTER UPDATE ON public.interests_quiz_responses
  FOR EACH ROW
  EXECUTE FUNCTION trigger_compute_interests();

-- ================================================
-- 9. Grant permissions
-- ================================================
GRANT ALL ON public.interests_quiz_questions TO authenticated;
GRANT ALL ON public.interests_quiz_responses TO authenticated;
GRANT ALL ON public.interests_quiz_answers TO authenticated;
GRANT ALL ON public.user_interests TO authenticated;

-- ================================================
-- SUCCESS MESSAGE
-- ================================================
DO $$
BEGIN
  RAISE NOTICE '';
  RAISE NOTICE '========================================';
  RAISE NOTICE '✅ INTERESTS QUIZ TABLES CREATED';
  RAISE NOTICE '========================================';
  RAISE NOTICE '';
  RAISE NOTICE 'Created tables:';
  RAISE NOTICE '1. interests_quiz_questions - Store quiz questions';
  RAISE NOTICE '2. interests_quiz_responses - Track quiz sessions';
  RAISE NOTICE '3. interests_quiz_answers - Store individual answers (row-based)';
  RAISE NOTICE '4. user_interests - Computed interest scores';
  RAISE NOTICE '';
  RAISE NOTICE 'Benefits of row-based storage:';
  RAISE NOTICE '- Questions can be added/removed without schema changes';
  RAISE NOTICE '- Historical data preserved when questions change';
  RAISE NOTICE '- Flexible question types supported';
  RAISE NOTICE '- Easy to analyze patterns across users';
  RAISE NOTICE '========================================';
END $$;