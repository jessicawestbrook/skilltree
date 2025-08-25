-- Achievement System Database Schema
-- Track user achievements and milestones

-- 1. Create achievements table (defines all possible achievements)
CREATE TABLE IF NOT EXISTS achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Achievement details
  code TEXT UNIQUE NOT NULL, -- Unique identifier like 'first_lesson', 'streak_7'
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  category TEXT NOT NULL CHECK (category IN ('learning', 'streak', 'mastery', 'collection', 'social', 'special')),
  
  -- Achievement requirements
  requirement_type TEXT NOT NULL CHECK (requirement_type IN ('count', 'streak', 'score', 'collection', 'special')),
  requirement_value INTEGER, -- e.g., 7 for 7-day streak, 100 for 100 flashcards
  requirement_data JSONB DEFAULT '{}', -- Additional requirements
  
  -- Display
  icon TEXT, -- Icon name or emoji
  badge_color TEXT DEFAULT 'gold', -- Color theme for the badge
  rarity TEXT CHECK (rarity IN ('common', 'uncommon', 'rare', 'epic', 'legendary')) DEFAULT 'common',
  points INTEGER DEFAULT 10, -- Achievement points/XP
  
  -- Status
  is_active BOOLEAN DEFAULT true,
  is_secret BOOLEAN DEFAULT false, -- Hidden until unlocked
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create user_achievements table (tracks which achievements users have earned)
CREATE TABLE IF NOT EXISTS user_achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  achievement_id UUID REFERENCES achievements(id) ON DELETE CASCADE,
  
  -- Progress tracking
  current_progress INTEGER DEFAULT 0,
  target_progress INTEGER DEFAULT 1,
  progress_data JSONB DEFAULT '{}', -- Store detailed progress info
  
  -- Unlock details
  unlocked_at TIMESTAMP WITH TIME ZONE,
  notification_sent BOOLEAN DEFAULT false,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Ensure user can only have one record per achievement
  UNIQUE(user_id, achievement_id)
);

-- 3. Create user_stats table for tracking various statistics
CREATE TABLE IF NOT EXISTS user_stats (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- Learning stats
  total_lessons_completed INTEGER DEFAULT 0,
  total_flashcards_reviewed INTEGER DEFAULT 0,
  total_correct_answers INTEGER DEFAULT 0,
  total_study_time_minutes INTEGER DEFAULT 0,
  total_modules_completed INTEGER DEFAULT 0,
  
  -- Streak stats
  current_streak_days INTEGER DEFAULT 0,
  longest_streak_days INTEGER DEFAULT 0,
  last_activity_date DATE,
  
  -- Performance stats
  average_accuracy DECIMAL(5,2) DEFAULT 0,
  perfect_scores_count INTEGER DEFAULT 0,
  
  -- Collection stats
  total_achievements_unlocked INTEGER DEFAULT 0,
  total_achievement_points INTEGER DEFAULT 0,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Create indexes for performance
CREATE INDEX IF NOT EXISTS achievements_code_idx ON achievements(code);
CREATE INDEX IF NOT EXISTS achievements_category_idx ON achievements(category);
CREATE INDEX IF NOT EXISTS user_achievements_user_id_idx ON user_achievements(user_id);
CREATE INDEX IF NOT EXISTS user_achievements_achievement_id_idx ON user_achievements(achievement_id);
CREATE INDEX IF NOT EXISTS user_achievements_unlocked_at_idx ON user_achievements(unlocked_at);

-- 5. Enable RLS
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;

-- 6. Create RLS policies
-- Anyone can view achievements (to see what's available)
CREATE POLICY "Anyone can view achievements" ON achievements
  FOR SELECT USING (true);

-- Users can view their own achievement progress
CREATE POLICY "Users can view their own achievements" ON user_achievements
  FOR SELECT USING (auth.uid() = user_id);

-- System can create/update user achievements
CREATE POLICY "System can manage user achievements" ON user_achievements
  FOR ALL USING (true);

-- Users can view their own stats
CREATE POLICY "Users can view their own stats" ON user_stats
  FOR SELECT USING (auth.uid() = user_id);

-- System can manage user stats
CREATE POLICY "System can manage user stats" ON user_stats
  FOR ALL USING (true);

-- 7. Create trigger functions
CREATE OR REPLACE FUNCTION update_achievements_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_user_stats_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 8. Create triggers
DROP TRIGGER IF EXISTS update_achievements_updated_at_trigger ON achievements;
CREATE TRIGGER update_achievements_updated_at_trigger
  BEFORE UPDATE ON achievements
  FOR EACH ROW
  EXECUTE FUNCTION update_achievements_updated_at();

DROP TRIGGER IF EXISTS update_user_achievements_updated_at_trigger ON user_achievements;
CREATE TRIGGER update_user_achievements_updated_at_trigger
  BEFORE UPDATE ON user_achievements
  FOR EACH ROW
  EXECUTE FUNCTION update_achievements_updated_at();

DROP TRIGGER IF EXISTS update_user_stats_updated_at_trigger ON user_stats;
CREATE TRIGGER update_user_stats_updated_at_trigger
  BEFORE UPDATE ON user_stats
  FOR EACH ROW
  EXECUTE FUNCTION update_user_stats_updated_at();

-- 9. Insert initial achievements
INSERT INTO achievements (code, name, description, category, requirement_type, requirement_value, icon, badge_color, rarity, points) VALUES
-- Learning achievements
('first_lesson', 'First Steps', 'Complete your first lesson', 'learning', 'count', 1, '🎯', 'green', 'common', 10),
('lessons_10', 'Dedicated Learner', 'Complete 10 lessons', 'learning', 'count', 10, '📚', 'blue', 'common', 25),
('lessons_50', 'Knowledge Seeker', 'Complete 50 lessons', 'learning', 'count', 50, '🎓', 'purple', 'uncommon', 50),
('lessons_100', 'Scholar', 'Complete 100 lessons', 'learning', 'count', 100, '🏆', 'gold', 'rare', 100),
('lessons_500', 'Master Scholar', 'Complete 500 lessons', 'learning', 'count', 500, '👑', 'gold', 'epic', 250),
('lessons_1000', 'Grand Master', 'Complete 1000 lessons', 'learning', 'count', 1000, '💎', 'diamond', 'legendary', 500),

-- Streak achievements
('streak_3', 'Getting Started', 'Study for 3 days in a row', 'streak', 'streak', 3, '🔥', 'orange', 'common', 15),
('streak_7', 'Week Warrior', 'Study for 7 days in a row', 'streak', 'streak', 7, '⚡', 'yellow', 'common', 30),
('streak_14', 'Fortnight Fighter', 'Study for 14 days in a row', 'streak', 'streak', 14, '💪', 'orange', 'uncommon', 50),
('streak_30', 'Monthly Master', 'Study for 30 days in a row', 'streak', 'streak', 30, '🌟', 'gold', 'rare', 100),
('streak_100', 'Century Club', 'Study for 100 days in a row', 'streak', 'streak', 100, '💯', 'platinum', 'epic', 300),
('streak_365', 'Year of Learning', 'Study for 365 days in a row', 'streak', 'streak', 365, '🌈', 'rainbow', 'legendary', 1000),

-- Flashcard mastery achievements
('flashcards_10', 'Card Collector', 'Review 10 flashcards', 'mastery', 'count', 10, '🃏', 'blue', 'common', 10),
('flashcards_100', 'Card Master', 'Review 100 flashcards', 'mastery', 'count', 100, '🎴', 'purple', 'uncommon', 30),
('flashcards_1000', 'Card Legend', 'Review 1000 flashcards', 'mastery', 'count', 1000, '🎭', 'gold', 'rare', 100),
('perfect_10', 'Perfect Ten', 'Get 10 flashcards correct in a row', 'mastery', 'count', 10, '✨', 'silver', 'uncommon', 25),
('perfect_25', 'Precision Expert', 'Get 25 flashcards correct in a row', 'mastery', 'count', 25, '🎯', 'gold', 'rare', 50),
('perfect_50', 'Flawless Victory', 'Get 50 flashcards correct in a row', 'mastery', 'count', 50, '💫', 'platinum', 'epic', 100),

-- Module completion achievements
('module_first', 'Module Explorer', 'Complete your first module', 'learning', 'count', 1, '🗺️', 'green', 'common', 20),
('module_5', 'Module Navigator', 'Complete 5 modules', 'learning', 'count', 5, '🧭', 'blue', 'common', 40),
('module_25', 'Module Expert', 'Complete 25 modules', 'learning', 'count', 25, '🚀', 'purple', 'uncommon', 75),
('module_100', 'Module Master', 'Complete 100 modules', 'learning', 'count', 100, '🌍', 'gold', 'rare', 200),

-- Special achievements
('night_owl', 'Night Owl', 'Study after midnight', 'special', 'special', 1, '🦉', 'purple', 'uncommon', 25),
('early_bird', 'Early Bird', 'Study before 6 AM', 'special', 'special', 1, '🐦', 'yellow', 'uncommon', 25),
('weekend_warrior', 'Weekend Warrior', 'Study on both Saturday and Sunday', 'special', 'special', 1, '⚔️', 'silver', 'common', 20),
('speed_demon', 'Speed Demon', 'Complete 10 flashcards in under 1 minute', 'special', 'special', 1, '⚡', 'red', 'rare', 50),
('comeback_kid', 'Comeback Kid', 'Return to studying after a 7+ day break', 'special', 'special', 1, '🔄', 'green', 'uncommon', 30),
('perfectionist', 'Perfectionist', 'Score 100% on 5 assessments', 'special', 'count', 5, '💯', 'gold', 'rare', 75),

-- Collection achievements
('diverse_learner', 'Diverse Learner', 'Study from 5 different categories', 'collection', 'collection', 5, '🌐', 'rainbow', 'uncommon', 40),
('polymath', 'Polymath', 'Study from 10 different categories', 'collection', 'collection', 10, '🧠', 'platinum', 'rare', 80),
('renaissance', 'Renaissance Mind', 'Study from 20 different categories', 'collection', 'collection', 20, '🎨', 'gold', 'epic', 150)

ON CONFLICT (code) DO NOTHING; -- Don't duplicate if already exists