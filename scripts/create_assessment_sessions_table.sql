-- Create assessment_sessions table for adaptive assessments
CREATE TABLE IF NOT EXISTS assessment_sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  category_id UUID NOT NULL REFERENCES skill_tree_nodes(id) ON DELETE CASCADE,
  session_type VARCHAR(50) DEFAULT 'assessment',
  status VARCHAR(50) DEFAULT 'active',
  current_ability_estimate DECIMAL(5,2) DEFAULT 0,
  confidence_interval DECIMAL(5,2) DEFAULT 1,
  total_questions INTEGER DEFAULT 0,
  correct_answers INTEGER DEFAULT 0,
  total_points INTEGER DEFAULT 0,
  streak_count INTEGER DEFAULT 0,
  max_streak INTEGER DEFAULT 0,
  highest_difficulty_reached INTEGER DEFAULT 0,
  started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_assessment_sessions_user_id ON assessment_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_assessment_sessions_category_id ON assessment_sessions(category_id);
CREATE INDEX IF NOT EXISTS idx_assessment_sessions_status ON assessment_sessions(status);
CREATE INDEX IF NOT EXISTS idx_assessment_sessions_user_category ON assessment_sessions(user_id, category_id);

-- Create question responses table for tracking individual answers
CREATE TABLE IF NOT EXISTS assessment_question_responses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id UUID NOT NULL REFERENCES assessment_sessions(id) ON DELETE CASCADE,
  question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
  user_response TEXT,
  is_correct BOOLEAN DEFAULT FALSE,
  response_time_ms INTEGER,
  difficulty_level INTEGER,
  points_earned INTEGER DEFAULT 0,
  question_sequence INTEGER,
  point_multipliers JSONB DEFAULT '{}',
  answered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for question responses
CREATE INDEX IF NOT EXISTS idx_assessment_responses_session_id ON assessment_question_responses(session_id);
CREATE INDEX IF NOT EXISTS idx_assessment_responses_question_id ON assessment_question_responses(question_id);

-- Grant permissions
GRANT ALL ON assessment_sessions TO authenticated;
GRANT ALL ON assessment_question_responses TO authenticated;

-- Enable RLS
ALTER TABLE assessment_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_question_responses ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view own assessment sessions" ON assessment_sessions
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own assessment sessions" ON assessment_sessions
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own assessment sessions" ON assessment_sessions
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own question responses" ON assessment_question_responses
  FOR SELECT USING (session_id IN (SELECT id FROM assessment_sessions WHERE user_id = auth.uid()));

CREATE POLICY "Users can create own question responses" ON assessment_question_responses
  FOR INSERT WITH CHECK (session_id IN (SELECT id FROM assessment_sessions WHERE user_id = auth.uid()));