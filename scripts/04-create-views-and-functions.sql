-- ================================================
-- STEP 4: CREATE VIEWS, FUNCTIONS, AND TRIGGERS
-- ================================================
-- Run this AFTER 03-create-user-tables.sql
-- Creates views, functions, and triggers
-- ================================================

-- ================================================
-- VIEWS
-- ================================================

-- Drop and recreate leaderboard view
DROP VIEW IF EXISTS leaderboard CASCADE;
CREATE VIEW leaderboard AS
SELECT 
  up.id as user_id,
  up.username,
  up.display_name,
  up.avatar_url,
  up.total_points,
  up.neural_level,
  up.total_nodes_completed,
  up.title,
  RANK() OVER (ORDER BY up.total_points DESC) as global_rank,
  RANK() OVER (PARTITION BY up.favorite_domain ORDER BY up.total_points DESC) as domain_rank
FROM user_profiles up
WHERE up.total_points > 0
ORDER BY up.total_points DESC
LIMIT 100;

-- View for nodes with their prerequisite count
DROP VIEW IF EXISTS nodes_with_prereq_count CASCADE;
CREATE VIEW nodes_with_prereq_count AS
SELECT 
  kn.*,
  COALESCE(prereq_counts.prereq_count, 0) as prerequisite_count
FROM knowledge_nodes kn
LEFT JOIN (
  SELECT node_id, COUNT(*) as prereq_count
  FROM node_prerequisites
  GROUP BY node_id
) prereq_counts ON kn.id = prereq_counts.node_id;

-- View for learning paths with node details
DROP VIEW IF EXISTS learning_paths_detailed CASCADE;
CREATE VIEW learning_paths_detailed AS
SELECT 
  lp.id as path_id,
  lp.name as path_name,
  lp.description,
  lp.icon_name,
  lpn.order_index,
  kn.*
FROM learning_paths lp
JOIN learning_path_nodes lpn ON lp.id = lpn.path_id
JOIN knowledge_nodes kn ON lpn.node_id = kn.id
ORDER BY lp.id, lpn.order_index;

-- ================================================
-- HELPER FUNCTIONS
-- ================================================

-- Function to get user's completed nodes
CREATE OR REPLACE FUNCTION get_user_completed_nodes(p_user_id UUID)
RETURNS TABLE(node_id VARCHAR(255), completed_at TIMESTAMP WITH TIME ZONE, points_earned INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT up.node_id, up.completed_at, up.points_earned
  FROM user_progress up
  WHERE up.user_id = p_user_id
  ORDER BY up.completed_at DESC;
END;
$$;

-- Function to check if prerequisites are met for a node
CREATE OR REPLACE FUNCTION check_prerequisites_met(p_user_id UUID, p_node_id VARCHAR(255))
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
  prereq_count INTEGER;
  completed_prereq_count INTEGER;
BEGIN
  -- Count total prerequisites for the node
  SELECT COUNT(*)
  INTO prereq_count
  FROM node_prerequisites
  WHERE node_id = p_node_id;
  
  -- If no prerequisites, return true
  IF prereq_count = 0 THEN
    RETURN TRUE;
  END IF;
  
  -- Count completed prerequisites
  SELECT COUNT(*)
  INTO completed_prereq_count
  FROM node_prerequisites np
  INNER JOIN user_progress up ON up.node_id = np.prerequisite_id
  WHERE np.node_id = p_node_id
    AND up.user_id = p_user_id;
  
  -- Return true if all prerequisites are completed
  RETURN prereq_count = completed_prereq_count;
END;
$$;

-- Function to calculate user level based on points
CREATE OR REPLACE FUNCTION calculate_user_level(p_points INTEGER)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
BEGIN
  -- Simple level calculation: every 500 points = 1 level
  RETURN GREATEST(1, FLOOR(p_points / 500) + 1);
END;
$$;

-- ================================================
-- TRIGGER FUNCTIONS
-- ================================================

-- Auto-create user profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  -- Check if profile already exists
  IF EXISTS (SELECT 1 FROM public.user_profiles WHERE id = NEW.id) THEN
    -- Update existing profile
    UPDATE public.user_profiles 
    SET last_active_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
  ELSE
    -- Insert new profile
    INSERT INTO public.user_profiles (id, username, display_name, avatar_url)
    VALUES (
      NEW.id,
      COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
      COALESCE(NEW.raw_user_meta_data->>'display_name', split_part(NEW.email, '@', 1)),
      COALESCE(NEW.raw_user_meta_data->>'avatar_url', 'https://api.dicebear.com/7.x/avataaars/svg?seed=' || NEW.id)
    );
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Update profile stats function
CREATE OR REPLACE FUNCTION update_profile_stats()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE user_profiles
  SET 
    total_points = total_points + NEW.points_earned,
    neural_level = GREATEST(1, FLOOR((total_points + NEW.points_earned) / 500) + 1),
    total_nodes_completed = total_nodes_completed + 1,
    last_active_at = CURRENT_TIMESTAMP,
    updated_at = CURRENT_TIMESTAMP
  WHERE id = NEW.user_id;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Update user_stats when progress is added
CREATE OR REPLACE FUNCTION update_user_stats_on_progress()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  -- Check if user stats exist
  IF EXISTS (SELECT 1 FROM user_stats WHERE user_id = NEW.user_id) THEN
    -- Update existing stats
    UPDATE user_stats
    SET 
      total_points = total_points + NEW.points_earned,
      neural_level = calculate_user_level(total_points + NEW.points_earned),
      total_nodes_completed = total_nodes_completed + 1,
      last_activity_date = CURRENT_DATE,
      updated_at = CURRENT_TIMESTAMP
    WHERE user_id = NEW.user_id;
  ELSE
    -- Insert new stats
    INSERT INTO user_stats (
      user_id,
      total_points,
      neural_level,
      total_nodes_completed,
      last_activity_date,
      updated_at
    )
    VALUES (
      NEW.user_id,
      NEW.points_earned,
      1,
      1,
      CURRENT_DATE,
      CURRENT_TIMESTAMP
    );
  END IF;
    
  RETURN NEW;
END;
$$;

-- Check achievements function
CREATE OR REPLACE FUNCTION check_achievements()
RETURNS TRIGGER AS $$
DECLARE
  achievement RECORD;
BEGIN
  FOR achievement IN SELECT * FROM achievements LOOP
    -- Check points-based achievements
    IF achievement.points_required > 0 AND NEW.total_points >= achievement.points_required THEN
      -- Only insert if not already earned
      IF NOT EXISTS (
        SELECT 1 FROM user_achievements 
        WHERE user_id = NEW.id AND achievement_id = achievement.id
      ) THEN
        INSERT INTO user_achievements (user_id, achievement_id)
        VALUES (NEW.id, achievement.id);
      END IF;
    END IF;
    
    -- Check nodes-based achievements
    IF achievement.nodes_required > 0 AND NEW.total_nodes_completed >= achievement.nodes_required THEN
      -- Only insert if not already earned
      IF NOT EXISTS (
        SELECT 1 FROM user_achievements 
        WHERE user_id = NEW.id AND achievement_id = achievement.id
      ) THEN
        INSERT INTO user_achievements (user_id, achievement_id)
        VALUES (NEW.id, achievement.id);
      END IF;
    END IF;
  END LOOP;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ================================================
-- CREATE TRIGGERS
-- ================================================

-- Drop and recreate triggers
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

DROP TRIGGER IF EXISTS trigger_update_profile_stats ON user_progress;
CREATE TRIGGER trigger_update_profile_stats
  AFTER INSERT ON user_progress
  FOR EACH ROW
  EXECUTE FUNCTION update_profile_stats();

DROP TRIGGER IF EXISTS trigger_update_user_stats ON user_progress;
CREATE TRIGGER trigger_update_user_stats
  AFTER INSERT ON user_progress
  FOR EACH ROW
  EXECUTE FUNCTION update_user_stats_on_progress();

DROP TRIGGER IF EXISTS trigger_check_achievements ON user_profiles;
CREATE TRIGGER trigger_check_achievements
  AFTER UPDATE OF total_points, total_nodes_completed ON user_profiles
  FOR EACH ROW
  EXECUTE FUNCTION check_achievements();

-- ================================================
-- VERIFICATION
-- ================================================

DO $$
BEGIN
  RAISE NOTICE 'Views, functions, and triggers created successfully!';
  RAISE NOTICE '';
  RAISE NOTICE '========================================';
  RAISE NOTICE 'DATABASE SCHEMA SETUP COMPLETE!';
  RAISE NOTICE '========================================';
  RAISE NOTICE '';
  RAISE NOTICE 'All tables created:';
  RAISE NOTICE '  - Core: knowledge_nodes, node_prerequisites, quiz_questions';
  RAISE NOTICE '  - Paths: learning_paths, learning_path_nodes';
  RAISE NOTICE '  - User: user_progress, user_stats, user_profiles';
  RAISE NOTICE '  - Gaming: achievements, user_achievements, user_connections';
  RAISE NOTICE '';
  RAISE NOTICE 'Views created:';
  RAISE NOTICE '  - leaderboard, nodes_with_prereq_count, learning_paths_detailed';
  RAISE NOTICE '';
  RAISE NOTICE 'Functions and triggers active';
  RAISE NOTICE '';
  RAISE NOTICE 'Next step: Run npm run migrate:all to populate with data';
END $$;