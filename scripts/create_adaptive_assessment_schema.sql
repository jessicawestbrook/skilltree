-- Computer Adaptive Testing (CAT) Database Schema
-- Created: 2025-08-21
-- Purpose: Support adaptive assessments with point-based scoring

-- ===================================
-- 1. Assessment Sessions Table
-- ===================================
CREATE TABLE IF NOT EXISTS assessment_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES skill_tree_nodes(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    total_points INTEGER DEFAULT 0,
    questions_answered INTEGER DEFAULT 0,
    highest_difficulty_reached INTEGER DEFAULT 1,
    final_ability_estimate DECIMAL(5,2) DEFAULT 0.0,
    session_type VARCHAR(20) DEFAULT 'practice', -- 'practice', 'assessment', 'quick_test'
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_assessment_sessions_user_id ON assessment_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_assessment_sessions_category_id ON assessment_sessions(category_id);
CREATE INDEX IF NOT EXISTS idx_assessment_sessions_started_at ON assessment_sessions(started_at);

-- ===================================
-- 2. Question Responses Table
-- ===================================
CREATE TABLE IF NOT EXISTS question_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    question_id UUID REFERENCES questions(id) ON DELETE CASCADE,
    user_response TEXT,
    is_correct BOOLEAN NOT NULL,
    response_time_ms INTEGER,
    difficulty_level INTEGER NOT NULL DEFAULT 2,
    points_earned INTEGER DEFAULT 0,
    question_sequence INTEGER NOT NULL,
    point_multipliers JSONB DEFAULT '{}', -- Store multiplier details
    answered_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_question_responses_session_id ON question_responses(session_id);
CREATE INDEX IF NOT EXISTS idx_question_responses_question_id ON question_responses(question_id);
CREATE INDEX IF NOT EXISTS idx_question_responses_difficulty ON question_responses(difficulty_level);

-- ===================================
-- 3. User Category Scores Table
-- ===================================
CREATE TABLE IF NOT EXISTS user_category_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES skill_tree_nodes(id) ON DELETE CASCADE,
    current_ability_estimate DECIMAL(5,2) DEFAULT 0.0,
    total_points INTEGER DEFAULT 0,
    best_session_points INTEGER DEFAULT 0,
    questions_answered_total INTEGER DEFAULT 0,
    sessions_completed INTEGER DEFAULT 0,
    last_assessment_date TIMESTAMPTZ,
    mastery_level INTEGER DEFAULT 1, -- 1-5 based on demonstrated ability
    achievement_badges JSONB DEFAULT '[]', -- Array of earned badges
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Ensure one record per user-category combination
    UNIQUE(user_id, category_id)
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_category_scores_user_id ON user_category_scores(user_id);
CREATE INDEX IF NOT EXISTS idx_user_category_scores_category_id ON user_category_scores(category_id);
CREATE INDEX IF NOT EXISTS idx_user_category_scores_mastery ON user_category_scores(mastery_level);

-- ===================================
-- 4. Question Difficulty Enhancement
-- ===================================
-- Add difficulty and timing columns to existing questions table
DO $$ 
BEGIN
    -- Add difficulty_level column if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'questions' AND column_name = 'difficulty_level') THEN
        ALTER TABLE questions ADD COLUMN difficulty_level INTEGER DEFAULT 2;
    END IF;
    
    -- Add estimated_time_seconds column if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'questions' AND column_name = 'estimated_time_seconds') THEN
        ALTER TABLE questions ADD COLUMN estimated_time_seconds INTEGER DEFAULT 60;
    END IF;
    
    -- Add cognitive_load_rating column if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'questions' AND column_name = 'cognitive_load_rating') THEN
        ALTER TABLE questions ADD COLUMN cognitive_load_rating INTEGER DEFAULT 3;
    END IF;
    
    -- Add last_used_at column for question selection optimization
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'questions' AND column_name = 'last_used_at') THEN
        ALTER TABLE questions ADD COLUMN last_used_at TIMESTAMPTZ;
    END IF;
    
    -- Add usage_count column for balancing question exposure
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'questions' AND column_name = 'usage_count') THEN
        ALTER TABLE questions ADD COLUMN usage_count INTEGER DEFAULT 0;
    END IF;
END $$;

-- Add index for difficulty-based queries
CREATE INDEX IF NOT EXISTS idx_questions_difficulty_level ON questions(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_questions_usage_count ON questions(usage_count);

-- ===================================
-- 5. User Question History Table
-- ===================================
-- Track which questions users have seen to avoid repetition
CREATE TABLE IF NOT EXISTS user_question_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    question_id UUID REFERENCES questions(id) ON DELETE CASCADE,
    category_id UUID REFERENCES skill_tree_nodes(id) ON DELETE CASCADE,
    times_seen INTEGER DEFAULT 1,
    times_correct INTEGER DEFAULT 0,
    last_seen_at TIMESTAMPTZ DEFAULT NOW(),
    last_correct_at TIMESTAMPTZ,
    average_response_time_ms INTEGER,
    
    -- Ensure one record per user-question combination
    UNIQUE(user_id, question_id)
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_question_history_user_id ON user_question_history(user_id);
CREATE INDEX IF NOT EXISTS idx_user_question_history_category_id ON user_question_history(category_id);
CREATE INDEX IF NOT EXISTS idx_user_question_history_last_seen ON user_question_history(last_seen_at);

-- ===================================
-- 6. Update Triggers
-- ===================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at columns
DROP TRIGGER IF EXISTS update_assessment_sessions_updated_at ON assessment_sessions;
CREATE TRIGGER update_assessment_sessions_updated_at 
    BEFORE UPDATE ON assessment_sessions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_category_scores_updated_at ON user_category_scores;
CREATE TRIGGER update_user_category_scores_updated_at 
    BEFORE UPDATE ON user_category_scores 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ===================================
-- 7. RLS (Row Level Security) Policies
-- ===================================

-- Enable RLS on all tables
ALTER TABLE assessment_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_responses ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_category_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_question_history ENABLE ROW LEVEL SECURITY;

-- Assessment Sessions Policies
DROP POLICY IF EXISTS "Users can view own assessment sessions" ON assessment_sessions;
CREATE POLICY "Users can view own assessment sessions" ON assessment_sessions
    FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can create own assessment sessions" ON assessment_sessions;
CREATE POLICY "Users can create own assessment sessions" ON assessment_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own assessment sessions" ON assessment_sessions;
CREATE POLICY "Users can update own assessment sessions" ON assessment_sessions
    FOR UPDATE USING (auth.uid() = user_id);

-- Question Responses Policies
DROP POLICY IF EXISTS "Users can view own question responses" ON question_responses;
CREATE POLICY "Users can view own question responses" ON question_responses
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM assessment_sessions 
            WHERE assessment_sessions.id = session_id 
            AND assessment_sessions.user_id = auth.uid()
        )
    );

DROP POLICY IF EXISTS "Users can create own question responses" ON question_responses;
CREATE POLICY "Users can create own question responses" ON question_responses
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM assessment_sessions 
            WHERE assessment_sessions.id = session_id 
            AND assessment_sessions.user_id = auth.uid()
        )
    );

-- User Category Scores Policies
DROP POLICY IF EXISTS "Users can view own category scores" ON user_category_scores;
CREATE POLICY "Users can view own category scores" ON user_category_scores
    FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own category scores" ON user_category_scores;
CREATE POLICY "Users can update own category scores" ON user_category_scores
    FOR ALL USING (auth.uid() = user_id);

-- User Question History Policies
DROP POLICY IF EXISTS "Users can view own question history" ON user_question_history;
CREATE POLICY "Users can view own question history" ON user_question_history
    FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own question history" ON user_question_history;
CREATE POLICY "Users can update own question history" ON user_question_history
    FOR ALL USING (auth.uid() = user_id);

-- ===================================
-- 8. Helper Functions
-- ===================================

-- Function to calculate points based on difficulty level
CREATE OR REPLACE FUNCTION calculate_base_points(difficulty_level INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN CASE difficulty_level
        WHEN 1 THEN 10   -- Beginner
        WHEN 2 THEN 25   -- Elementary
        WHEN 3 THEN 50   -- Intermediate
        WHEN 4 THEN 100  -- Advanced
        WHEN 5 THEN 200  -- Expert
        ELSE 25          -- Default to Elementary
    END;
END;
$$ LANGUAGE plpgsql;

-- Function to get user's current ability estimate for a category
CREATE OR REPLACE FUNCTION get_user_ability_estimate(p_user_id UUID, p_category_id UUID)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    ability_estimate DECIMAL(5,2);
BEGIN
    SELECT current_ability_estimate INTO ability_estimate
    FROM user_category_scores
    WHERE user_id = p_user_id AND category_id = p_category_id;
    
    RETURN COALESCE(ability_estimate, 0.0);
END;
$$ LANGUAGE plpgsql;

-- ===================================
-- 9. Initial Data Setup
-- ===================================

-- Insert difficulty level reference data (for documentation)
-- This could be a separate reference table if needed

-- ===================================
-- 10. Verification Queries
-- ===================================

-- Verify tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN (
    'assessment_sessions', 
    'question_responses', 
    'user_category_scores', 
    'user_question_history'
  )
ORDER BY table_name;

-- Verify question table enhancements
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'questions'
  AND column_name IN (
    'difficulty_level', 
    'estimated_time_seconds', 
    'cognitive_load_rating',
    'last_used_at',
    'usage_count'
  )
ORDER BY column_name;