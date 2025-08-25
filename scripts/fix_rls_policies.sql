-- Fix RLS policies for achievements and user_question_responses tables

-- Enable RLS on tables if not already enabled
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_question_responses ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Achievements are viewable by everyone" ON achievements;
DROP POLICY IF EXISTS "User achievements are viewable by owner" ON user_achievements;
DROP POLICY IF EXISTS "User achievements insertable by owner" ON user_achievements;
DROP POLICY IF EXISTS "User achievements updatable by owner" ON user_achievements;
DROP POLICY IF EXISTS "User stats viewable by owner" ON user_stats;
DROP POLICY IF EXISTS "User stats insertable by owner" ON user_stats;
DROP POLICY IF EXISTS "User stats updatable by owner" ON user_stats;
DROP POLICY IF EXISTS "Users can view own responses" ON user_question_responses;
DROP POLICY IF EXISTS "Users can insert own responses" ON user_question_responses;
DROP POLICY IF EXISTS "Users can update own responses" ON user_question_responses;

-- Achievements table - viewable by everyone
CREATE POLICY "Achievements are viewable by everyone" 
ON achievements FOR SELECT 
USING (true);

-- User achievements - users can view and manage their own
CREATE POLICY "User achievements are viewable by owner" 
ON user_achievements FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "User achievements insertable by owner" 
ON user_achievements FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "User achievements updatable by owner" 
ON user_achievements FOR UPDATE 
USING (auth.uid() = user_id);

-- User stats - users can view and manage their own
CREATE POLICY "User stats viewable by owner" 
ON user_stats FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "User stats insertable by owner" 
ON user_stats FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "User stats updatable by owner" 
ON user_stats FOR UPDATE 
USING (auth.uid() = user_id);

-- User question responses - users can view and manage their own
CREATE POLICY "Users can view own responses" 
ON user_question_responses FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own responses" 
ON user_question_responses FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own responses" 
ON user_question_responses FOR UPDATE 
USING (auth.uid() = user_id);

-- Grant necessary permissions
GRANT ALL ON achievements TO authenticated;
GRANT ALL ON user_achievements TO authenticated;
GRANT ALL ON user_stats TO authenticated;
GRANT ALL ON user_question_responses TO authenticated;

-- Also grant to anon for public read of achievements
GRANT SELECT ON achievements TO anon;