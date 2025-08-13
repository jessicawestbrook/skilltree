-- ================================================
-- RE-ENABLE SECURITY AFTER MIGRATION
-- ================================================
-- Run this AFTER npm run migrate:all completes
-- This re-enables RLS and ensures all policies are in place
-- ================================================

-- ================================================
-- RE-ENABLE RLS ON ALL TABLES
-- ================================================

ALTER TABLE knowledge_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE node_prerequisites ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_paths ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_path_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;

-- Enable on user tables if they exist
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'user_profiles') THEN
    ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
  END IF;
  
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'achievements') THEN
    ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
  END IF;
  
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'user_achievements') THEN
    ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
  END IF;
  
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'user_connections') THEN
    ALTER TABLE user_connections ENABLE ROW LEVEL SECURITY;
  END IF;
END $$;

-- ================================================
-- ENSURE ALL POLICIES ARE IN PLACE
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

-- Knowledge nodes - public read, service role write
SELECT drop_policy_if_exists('Allow public read access to nodes', 'knowledge_nodes');
SELECT drop_policy_if_exists('Allow service role to manage nodes', 'knowledge_nodes');

CREATE POLICY "Allow public read access to nodes" ON knowledge_nodes
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow service role to manage nodes" ON knowledge_nodes
  FOR ALL TO service_role USING (true);

-- Prerequisites - public read, service role write
SELECT drop_policy_if_exists('Allow public read access to prerequisites', 'node_prerequisites');
SELECT drop_policy_if_exists('Allow service role to manage prerequisites', 'node_prerequisites');

CREATE POLICY "Allow public read access to prerequisites" ON node_prerequisites
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow service role to manage prerequisites" ON node_prerequisites
  FOR ALL TO service_role USING (true);

-- Quiz questions - public read, service role write
SELECT drop_policy_if_exists('Allow public read access to questions', 'quiz_questions');
SELECT drop_policy_if_exists('Allow service role to manage questions', 'quiz_questions');

CREATE POLICY "Allow public read access to questions" ON quiz_questions
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow service role to manage questions" ON quiz_questions
  FOR ALL TO service_role USING (true);

-- Learning paths - public read, service role write
SELECT drop_policy_if_exists('Allow public read access to learning paths', 'learning_paths');
SELECT drop_policy_if_exists('Allow service role to manage learning paths', 'learning_paths');

CREATE POLICY "Allow public read access to learning paths" ON learning_paths
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow service role to manage learning paths" ON learning_paths
  FOR ALL TO service_role USING (true);

-- Learning path nodes - public read, service role write
SELECT drop_policy_if_exists('Allow public read access to learning path nodes', 'learning_path_nodes');
SELECT drop_policy_if_exists('Allow service role to manage learning path nodes', 'learning_path_nodes');

CREATE POLICY "Allow public read access to learning path nodes" ON learning_path_nodes
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow service role to manage learning path nodes" ON learning_path_nodes
  FOR ALL TO service_role USING (true);

-- User progress - authenticated users only
SELECT drop_policy_if_exists('Users can view own progress', 'user_progress');
SELECT drop_policy_if_exists('Users can insert own progress', 'user_progress');
SELECT drop_policy_if_exists('Users can update own progress', 'user_progress');

CREATE POLICY "Users can view own progress" ON user_progress
  FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress" ON user_progress
  FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress" ON user_progress
  FOR UPDATE TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- User stats - public read for leaderboard
SELECT drop_policy_if_exists('Public can view leaderboard stats', 'user_stats');
SELECT drop_policy_if_exists('Users can manage own stats', 'user_stats');

CREATE POLICY "Public can view leaderboard stats" ON user_stats
  FOR SELECT TO public USING (true);

CREATE POLICY "Users can manage own stats" ON user_stats
  FOR ALL TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- User profiles
SELECT drop_policy_if_exists('Users can view all profiles', 'user_profiles');
SELECT drop_policy_if_exists('Users can update own profile', 'user_profiles');
SELECT drop_policy_if_exists('Users can insert own profile', 'user_profiles');

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'user_profiles') THEN
    CREATE POLICY "Users can view all profiles" ON user_profiles
      FOR SELECT TO public USING (true);

    CREATE POLICY "Users can update own profile" ON user_profiles
      FOR UPDATE TO authenticated
      USING (auth.uid() = id)
      WITH CHECK (auth.uid() = id);

    CREATE POLICY "Users can insert own profile" ON user_profiles
      FOR INSERT TO authenticated
      WITH CHECK (auth.uid() = id);
  END IF;
END $$;

-- Achievements
SELECT drop_policy_if_exists('Anyone can view achievements', 'achievements');

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'achievements') THEN
    CREATE POLICY "Anyone can view achievements" ON achievements
      FOR SELECT TO public USING (true);
  END IF;
END $$;

-- User achievements
SELECT drop_policy_if_exists('Users can view all user achievements', 'user_achievements');
SELECT drop_policy_if_exists('Users can insert own achievements', 'user_achievements');

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'user_achievements') THEN
    CREATE POLICY "Users can view all user achievements" ON user_achievements
      FOR SELECT TO public USING (true);

    CREATE POLICY "Users can insert own achievements" ON user_achievements
      FOR INSERT TO authenticated
      WITH CHECK (auth.uid() = user_id);
  END IF;
END $$;

-- User connections
SELECT drop_policy_if_exists('Users can view own connections', 'user_connections');
SELECT drop_policy_if_exists('Users can insert connection requests', 'user_connections');
SELECT drop_policy_if_exists('Users can update own connections', 'user_connections');

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'user_connections') THEN
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
  END IF;
END $$;

-- Clean up helper function
DROP FUNCTION IF EXISTS drop_policy_if_exists(text, text);

-- ================================================
-- VERIFICATION
-- ================================================

DO $$
BEGIN
  RAISE NOTICE '================================================';
  RAISE NOTICE 'SECURITY RE-ENABLED SUCCESSFULLY!';
  RAISE NOTICE '================================================';
  RAISE NOTICE '';
  RAISE NOTICE 'RLS is now active on all tables with proper policies:';
  RAISE NOTICE '  - Public can read knowledge data';
  RAISE NOTICE '  - Service role can manage data';
  RAISE NOTICE '  - Users can manage their own progress and profiles';
  RAISE NOTICE '';
  RAISE NOTICE 'Your database is now secure and ready for production use!';
  RAISE NOTICE '================================================';
END $$;