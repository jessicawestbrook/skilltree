-- ================================================
-- STEP 3: CREATE USER PROFILE TABLES
-- ================================================
-- Run this AFTER 02-create-dependent-tables.sql
-- Creates user profile and achievement tables
-- ================================================

-- Create user_profiles table
CREATE TABLE IF NOT EXISTS public.user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username VARCHAR(50) UNIQUE,
  display_name VARCHAR(100),
  avatar_url TEXT,
  bio TEXT,
  preferred_language VARCHAR(10) DEFAULT 'en',
  theme VARCHAR(20) DEFAULT 'light',
  email_notifications BOOLEAN DEFAULT true,
  title VARCHAR(100) DEFAULT 'Knowledge Seeker',
  badge_ids JSONB DEFAULT '[]'::jsonb,
  achievement_ids JSONB DEFAULT '[]'::jsonb,
  friend_ids UUID[] DEFAULT ARRAY[]::UUID[],
  total_points INTEGER DEFAULT 0,
  neural_level INTEGER DEFAULT 1,
  memory_crystals INTEGER DEFAULT 0,
  synaptic_streak INTEGER DEFAULT 0,
  total_nodes_completed INTEGER DEFAULT 0,
  favorite_domain VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  last_active_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_profiles_username ON user_profiles(username);
CREATE INDEX IF NOT EXISTS idx_user_profiles_neural_level ON user_profiles(neural_level);
CREATE INDEX IF NOT EXISTS idx_user_profiles_total_points ON user_profiles(total_points);

-- Create achievements table
CREATE TABLE IF NOT EXISTS achievements (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  icon_name VARCHAR(50),
  points_required INTEGER DEFAULT 0,
  nodes_required INTEGER DEFAULT 0,
  special_condition JSONB,
  badge_color VARCHAR(7) DEFAULT '#667eea',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert default achievements (check existence first)
INSERT INTO achievements (name, description, points_required, nodes_required, icon_name) 
SELECT * FROM (VALUES
  ('First Steps', 'Complete your first node', 0, 1, 'Trophy'),
  ('Quick Learner', 'Complete 5 nodes', 0, 5, 'Star'),
  ('Knowledge Hunter', 'Earn 500 points', 500, 0, 'Target'),
  ('Neural Master', 'Reach Neural Level 5', 0, 0, 'Brain'),
  ('Polymath', 'Complete nodes in 5 different domains', 0, 0, 'Compass'),
  ('Perfectionist', 'Get 100% on 10 quizzes', 0, 0, 'CheckCircle'),
  ('Speed Demon', 'Complete 3 nodes in one day', 0, 0, 'Zap'),
  ('Marathon Mind', 'Maintain a 7-day streak', 0, 0, 'Flame')
) AS v(name, description, points_required, nodes_required, icon_name)
WHERE NOT EXISTS (
  SELECT 1 FROM achievements WHERE achievements.name = v.name
);

-- Create user_achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  achievement_id UUID NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
  earned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, achievement_id)
);

CREATE INDEX IF NOT EXISTS idx_user_achievements_user_id ON user_achievements(user_id);

-- Create user_connections table
CREATE TABLE IF NOT EXISTS user_connections (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  friend_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  accepted_at TIMESTAMP WITH TIME ZONE,
  UNIQUE(user_id, friend_id),
  CHECK (user_id != friend_id)
);

CREATE INDEX IF NOT EXISTS idx_user_connections_user_id ON user_connections(user_id);
CREATE INDEX IF NOT EXISTS idx_user_connections_friend_id ON user_connections(friend_id);
CREATE INDEX IF NOT EXISTS idx_user_connections_status ON user_connections(status);

-- ================================================
-- Enable RLS
-- ================================================

ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_connections ENABLE ROW LEVEL SECURITY;

-- ================================================
-- Create policies
-- ================================================

-- Helper function to safely drop policies
CREATE OR REPLACE FUNCTION drop_policy_if_exists(
  policy_name text,
  table_name text
) RETURNS void AS $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE schemaname = 'public' 
    AND tablename = table_name 
    AND policyname = policy_name
  ) THEN
    EXECUTE format('DROP POLICY %I ON %I', policy_name, table_name);
  END IF;
END;
$$ LANGUAGE plpgsql;

-- User profiles policies
SELECT drop_policy_if_exists('Users can view all profiles', 'user_profiles');
SELECT drop_policy_if_exists('Users can update own profile', 'user_profiles');
SELECT drop_policy_if_exists('Users can insert own profile', 'user_profiles');

CREATE POLICY "Users can view all profiles" ON user_profiles
  FOR SELECT TO public USING (true);

CREATE POLICY "Users can update own profile" ON user_profiles
  FOR UPDATE TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON user_profiles
  FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = id);

-- Achievements policies
SELECT drop_policy_if_exists('Anyone can view achievements', 'achievements');
CREATE POLICY "Anyone can view achievements" ON achievements
  FOR SELECT TO public USING (true);

-- User achievements policies
SELECT drop_policy_if_exists('Users can view all user achievements', 'user_achievements');
SELECT drop_policy_if_exists('Users can insert own achievements', 'user_achievements');

CREATE POLICY "Users can view all user achievements" ON user_achievements
  FOR SELECT TO public USING (true);

CREATE POLICY "Users can insert own achievements" ON user_achievements
  FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- User connections policies
SELECT drop_policy_if_exists('Users can view own connections', 'user_connections');
SELECT drop_policy_if_exists('Users can insert connection requests', 'user_connections');
SELECT drop_policy_if_exists('Users can update own connections', 'user_connections');

CREATE POLICY "Users can view own connections" ON user_connections
  FOR SELECT TO authenticated
  USING (auth.uid() = user_id OR auth.uid() = friend_id);

CREATE POLICY "Users can insert connection requests" ON user_connections
  FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own connections" ON user_connections
  FOR UPDATE TO authenticated
  USING (auth.uid() = user_id OR auth.uid() = friend_id)
  WITH CHECK (auth.uid() = user_id OR auth.uid() = friend_id);

-- Clean up helper function
DROP FUNCTION IF EXISTS drop_policy_if_exists(text, text);

-- ================================================
-- Verification
-- ================================================

DO $$
BEGIN
  RAISE NOTICE 'User tables created successfully!';
  RAISE NOTICE 'Tables created: user_profiles, achievements, user_achievements, user_connections';
  RAISE NOTICE '';
  RAISE NOTICE 'Next: Run 04-create-views-and-functions.sql';
END $$;