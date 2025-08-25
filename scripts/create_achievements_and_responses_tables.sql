-- Create achievements system tables and user_question_responses table

-- Create achievements table
CREATE TABLE IF NOT EXISTS achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(100) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  category VARCHAR(50) NOT NULL CHECK (category IN ('learning', 'streak', 'mastery', 'collection', 'social', 'special')),
  requirement_type VARCHAR(50) NOT NULL CHECK (requirement_type IN ('count', 'streak', 'score', 'collection', 'special')),
  requirement_value INTEGER,
  requirement_data JSONB,
  icon VARCHAR(10) DEFAULT '🏆',
  badge_color VARCHAR(50) DEFAULT 'gold',
  rarity VARCHAR(50) NOT NULL CHECK (rarity IN ('common', 'uncommon', 'rare', 'epic', 'legendary')),
  points INTEGER NOT NULL DEFAULT 10,
  is_active BOOLEAN DEFAULT true,
  is_secret BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create user_achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  achievement_id UUID NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
  current_progress INTEGER DEFAULT 0,
  target_progress INTEGER DEFAULT 1,
  progress_data JSONB,
  unlocked_at TIMESTAMPTZ,
  notification_sent BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, achievement_id)
);

-- Create user_stats table
CREATE TABLE IF NOT EXISTS user_stats (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  total_lessons_completed INTEGER DEFAULT 0,
  total_flashcards_reviewed INTEGER DEFAULT 0,
  total_correct_answers INTEGER DEFAULT 0,
  total_study_time_minutes INTEGER DEFAULT 0,
  total_modules_completed INTEGER DEFAULT 0,
  current_streak_days INTEGER DEFAULT 0,
  longest_streak_days INTEGER DEFAULT 0,
  last_activity_date DATE,
  average_accuracy DECIMAL(5,2) DEFAULT 0,
  perfect_scores_count INTEGER DEFAULT 0,
  total_achievements_unlocked INTEGER DEFAULT 0,
  total_achievement_points INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create user_question_responses table
CREATE TABLE IF NOT EXISTS user_question_responses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
  session_id UUID NOT NULL,
  context_type VARCHAR(50) NOT NULL,
  context_id UUID,
  selected_answer INTEGER,
  is_correct BOOLEAN,
  time_spent_seconds INTEGER,
  question_sequence INTEGER,
  response_metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_achievements_user_id ON user_achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_user_achievements_achievement_id ON user_achievements(achievement_id);
CREATE INDEX IF NOT EXISTS idx_user_achievements_unlocked_at ON user_achievements(unlocked_at);
CREATE INDEX IF NOT EXISTS idx_user_question_responses_user_id ON user_question_responses(user_id);
CREATE INDEX IF NOT EXISTS idx_user_question_responses_question_id ON user_question_responses(question_id);
CREATE INDEX IF NOT EXISTS idx_user_question_responses_session_id ON user_question_responses(session_id);
CREATE INDEX IF NOT EXISTS idx_user_question_responses_context ON user_question_responses(context_type, context_id);

-- Enable RLS on all tables
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

-- Create RLS policies for achievements table
CREATE POLICY "Achievements are viewable by everyone" 
ON achievements FOR SELECT 
USING (true);

-- Create RLS policies for user_achievements table
CREATE POLICY "User achievements are viewable by owner" 
ON user_achievements FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "User achievements insertable by owner" 
ON user_achievements FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "User achievements updatable by owner" 
ON user_achievements FOR UPDATE 
USING (auth.uid() = user_id);

-- Create RLS policies for user_stats table
CREATE POLICY "User stats viewable by owner" 
ON user_stats FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "User stats insertable by owner" 
ON user_stats FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "User stats updatable by owner" 
ON user_stats FOR UPDATE 
USING (auth.uid() = user_id);

-- Create RLS policies for user_question_responses table
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
GRANT SELECT ON achievements TO anon;

-- Insert sample achievements
INSERT INTO achievements (code, name, description, category, requirement_type, requirement_value, icon, badge_color, rarity, points) VALUES
-- Learning achievements
('first_lesson', 'First Steps', 'Complete your first lesson', 'learning', 'count', 1, '👶', 'green', 'common', 10),
('lessons_10', 'Dedicated Learner', 'Complete 10 lessons', 'learning', 'count', 10, '📚', 'blue', 'common', 25),
('lessons_50', 'Knowledge Seeker', 'Complete 50 lessons', 'learning', 'count', 50, '🎓', 'purple', 'uncommon', 50),
('lessons_100', 'Scholar', 'Complete 100 lessons', 'learning', 'count', 100, '🏛️', 'gold', 'rare', 100),
('lessons_500', 'Master Scholar', 'Complete 500 lessons', 'learning', 'count', 500, '🌟', 'diamond', 'epic', 250),
('lessons_1000', 'Legendary Scholar', 'Complete 1000 lessons', 'learning', 'count', 1000, '💎', 'rainbow', 'legendary', 500),

-- Flashcard achievements
('flashcards_10', 'Card Novice', 'Review 10 flashcards', 'learning', 'count', 10, '🃏', 'green', 'common', 10),
('flashcards_100', 'Card Expert', 'Review 100 flashcards', 'learning', 'count', 100, '🎴', 'blue', 'uncommon', 30),
('flashcards_1000', 'Card Master', 'Review 1000 flashcards', 'learning', 'count', 1000, '🎯', 'purple', 'rare', 100),

-- Module completion achievements
('module_first', 'Module Explorer', 'Complete your first module', 'mastery', 'count', 1, '🗺️', 'green', 'common', 15),
('module_5', 'Module Adventurer', 'Complete 5 modules', 'mastery', 'count', 5, '🧭', 'blue', 'uncommon', 40),
('module_25', 'Module Conqueror', 'Complete 25 modules', 'mastery', 'count', 25, '⚔️', 'purple', 'rare', 100),
('module_100', 'Module Legend', 'Complete 100 modules', 'mastery', 'count', 100, '👑', 'gold', 'epic', 300),

-- Streak achievements
('streak_3', 'Consistent', '3 day learning streak', 'streak', 'streak', 3, '🔥', 'orange', 'common', 15),
('streak_7', 'Week Warrior', '7 day learning streak', 'streak', 'streak', 7, '📅', 'blue', 'common', 30),
('streak_30', 'Monthly Master', '30 day learning streak', 'streak', 'streak', 30, '📆', 'purple', 'uncommon', 100),
('streak_100', 'Century Club', '100 day learning streak', 'streak', 'streak', 100, '💯', 'gold', 'rare', 300),
('streak_365', 'Year of Learning', '365 day learning streak', 'streak', 'streak', 365, '🎊', 'rainbow', 'legendary', 1000),

-- Perfect score achievements
('perfectionist', 'Perfectionist', 'Get 10 perfect scores', 'mastery', 'count', 10, '💯', 'gold', 'uncommon', 50),
('perfect_10', 'Perfect Streak', 'Get 10 correct answers in a row', 'special', 'special', 10, '⭐', 'gold', 'uncommon', 40),
('perfect_25', 'Flawless', 'Get 25 correct answers in a row', 'special', 'special', 25, '🌟', 'diamond', 'rare', 100),
('perfect_50', 'Unstoppable', 'Get 50 correct answers in a row', 'special', 'special', 50, '💫', 'rainbow', 'epic', 250),

-- Collection achievements
('explorer_3', 'Explorer', 'Study from 3 different categories', 'collection', 'collection', 3, '🗺️', 'green', 'common', 20),
('explorer_10', 'Adventurer', 'Study from 10 different categories', 'collection', 'collection', 10, '🧭', 'blue', 'uncommon', 50),
('explorer_25', 'Renaissance Mind', 'Study from 25 different categories', 'collection', 'collection', 25, '🎨', 'purple', 'rare', 150),

-- Special time-based achievements
('night_owl', 'Night Owl', 'Complete a study session between midnight and 5 AM', 'special', 'special', 1, '🦉', 'purple', 'uncommon', 30),
('early_bird', 'Early Bird', 'Complete a study session before 6 AM', 'special', 'special', 1, '🐦', 'yellow', 'uncommon', 30),
('weekend_warrior', 'Weekend Warrior', 'Study on both Saturday and Sunday', 'special', 'special', 1, '⚔️', 'blue', 'common', 20),

-- Speed achievements
('speed_demon', 'Speed Demon', 'Complete 10 flashcards in under 60 seconds', 'special', 'special', 1, '⚡', 'yellow', 'rare', 75),

-- Comeback achievement
('comeback_kid', 'Comeback Kid', 'Return to studying after a week away', 'special', 'special', 1, '🔄', 'green', 'uncommon', 40)
ON CONFLICT (code) DO NOTHING;