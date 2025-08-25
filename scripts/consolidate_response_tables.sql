-- Consolidate response tables into a single unified table
-- Run this script in Supabase SQL Editor

-- Step 1: Create the unified table
CREATE TABLE IF NOT EXISTS public.user_question_responses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- Context information
  context_type TEXT NOT NULL CHECK (context_type IN ('assessment', 'practice', 'test', 'quiz', 'review', 'visual_test')),
  session_id UUID, -- Optional: links to assessment_sessions or study_sessions
  
  -- Question information
  question_id UUID NOT NULL,
  question_type TEXT, -- 'multiple_choice', 'true_false', 'visual_pattern', etc.
  question_sequence INTEGER, -- Order in session/test
  
  -- Response information
  user_response TEXT, -- The answer they selected
  is_correct BOOLEAN NOT NULL,
  response_time_ms INTEGER, -- Time taken in milliseconds
  
  -- Scoring
  difficulty_level INTEGER CHECK (difficulty_level >= 1 AND difficulty_level <= 5),
  points_earned INTEGER DEFAULT 0,
  point_multipliers JSONB, -- Store any multipliers applied
  
  -- Metadata
  attempt_number INTEGER DEFAULT 1, -- For tracking retries
  category_id UUID, -- Optional: which skill category
  metadata JSONB, -- Additional flexible data storage
  
  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  
  -- Indexes for common queries
  CONSTRAINT unique_session_question UNIQUE(session_id, question_id, attempt_number)
);

-- Step 2: Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_question_responses_user_id ON user_question_responses(user_id);
CREATE INDEX IF NOT EXISTS idx_user_question_responses_session_id ON user_question_responses(session_id);
CREATE INDEX IF NOT EXISTS idx_user_question_responses_question_id ON user_question_responses(question_id);
CREATE INDEX IF NOT EXISTS idx_user_question_responses_context_type ON user_question_responses(context_type);
CREATE INDEX IF NOT EXISTS idx_user_question_responses_created_at ON user_question_responses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_question_responses_category_id ON user_question_responses(category_id);

-- Step 3: Enable Row Level Security
ALTER TABLE user_question_responses ENABLE ROW LEVEL SECURITY;

-- Step 4: Create RLS policies
-- Users can view their own responses
CREATE POLICY "Users can view own responses" ON user_question_responses
  FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own responses
CREATE POLICY "Users can insert own responses" ON user_question_responses
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own responses (for practice mode)
CREATE POLICY "Users can update own responses" ON user_question_responses
  FOR UPDATE
  USING (auth.uid() = user_id AND context_type = 'practice');

-- Step 5: Grant permissions
GRANT ALL ON user_question_responses TO authenticated;
GRANT ALL ON user_question_responses TO service_role;

-- Step 6: Create function to get user statistics
CREATE OR REPLACE FUNCTION get_user_response_stats(p_user_id UUID, p_context_type TEXT DEFAULT NULL)
RETURNS TABLE (
  total_questions INTEGER,
  correct_answers INTEGER,
  accuracy_percentage NUMERIC,
  avg_response_time_ms INTEGER,
  total_points INTEGER
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    COUNT(*)::INTEGER as total_questions,
    COUNT(*) FILTER (WHERE is_correct)::INTEGER as correct_answers,
    ROUND(COUNT(*) FILTER (WHERE is_correct)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 2) as accuracy_percentage,
    AVG(response_time_ms)::INTEGER as avg_response_time_ms,
    SUM(points_earned)::INTEGER as total_points
  FROM user_question_responses
  WHERE user_id = p_user_id
    AND (p_context_type IS NULL OR context_type = p_context_type);
END;
$$ LANGUAGE plpgsql;

-- Step 7: Comment the table for documentation
COMMENT ON TABLE user_question_responses IS 'Unified table for all user question responses across different contexts (assessments, practice, tests, etc.)';
COMMENT ON COLUMN user_question_responses.context_type IS 'The context in which the question was answered: assessment, practice, test, quiz, review, visual_test';
COMMENT ON COLUMN user_question_responses.session_id IS 'Optional reference to assessment_sessions or study_sessions table';
COMMENT ON COLUMN user_question_responses.metadata IS 'Flexible JSONB field for storing additional context-specific data';

-- Step 8: Drop the old unused tables (ONLY RUN AFTER CONFIRMING MIGRATION)
-- IMPORTANT: These tables should be empty before dropping
-- Uncomment these lines only after verifying the migration is complete

-- DROP TABLE IF EXISTS question_responses CASCADE;
-- DROP TABLE IF EXISTS assessment_question_responses CASCADE;
-- DROP TABLE IF EXISTS user_test_responses CASCADE;
-- DROP TABLE IF EXISTS user_question_attempts CASCADE;

-- To verify tables are empty before dropping, run:
-- SELECT 'question_responses' as table_name, COUNT(*) as row_count FROM question_responses
-- UNION ALL
-- SELECT 'assessment_question_responses', COUNT(*) FROM assessment_question_responses
-- UNION ALL
-- SELECT 'user_test_responses', COUNT(*) FROM user_test_responses
-- UNION ALL
-- SELECT 'user_question_attempts', COUNT(*) FROM user_question_attempts;