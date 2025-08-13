-- ================================================
-- PREPARE DATABASE FOR MIGRATION
-- ================================================
-- Run this BEFORE running npm run migrate:all
-- This temporarily disables RLS to allow data insertion
-- ================================================

-- Temporarily disable RLS on all tables to allow migration
ALTER TABLE knowledge_nodes DISABLE ROW LEVEL SECURITY;
ALTER TABLE node_prerequisites DISABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_questions DISABLE ROW LEVEL SECURITY;
ALTER TABLE learning_paths DISABLE ROW LEVEL SECURITY;
ALTER TABLE learning_path_nodes DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats DISABLE ROW LEVEL SECURITY;

-- Also disable on user tables if they exist
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'user_profiles') THEN
    ALTER TABLE user_profiles DISABLE ROW LEVEL SECURITY;
  END IF;
  
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'achievements') THEN
    ALTER TABLE achievements DISABLE ROW LEVEL SECURITY;
  END IF;
  
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'user_achievements') THEN
    ALTER TABLE user_achievements DISABLE ROW LEVEL SECURITY;
  END IF;
  
  IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'user_connections') THEN
    ALTER TABLE user_connections DISABLE ROW LEVEL SECURITY;
  END IF;
END $$;

DO $$
BEGIN
  RAISE NOTICE '================================================';
  RAISE NOTICE 'RLS TEMPORARILY DISABLED FOR MIGRATION';
  RAISE NOTICE '================================================';
  RAISE NOTICE '';
  RAISE NOTICE 'You can now run: npm run migrate:all';
  RAISE NOTICE '';
  RAISE NOTICE 'After migration completes, run:';
  RAISE NOTICE '  05-enable-security.sql';
  RAISE NOTICE '================================================';
END $$;