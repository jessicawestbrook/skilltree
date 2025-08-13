-- ================================================
-- USER PROGRESS FUNCTIONS
-- ================================================
-- Functions to handle user progress and stats updates
-- ================================================

-- Create function to update user stats
CREATE OR REPLACE FUNCTION update_user_stats(
  p_user_id UUID,
  p_points INTEGER,
  p_node_completed BOOLEAN DEFAULT FALSE
)
RETURNS void AS $$
BEGIN
  UPDATE user_profiles
  SET 
    total_points = total_points + p_points,
    total_nodes_completed = CASE 
      WHEN p_node_completed THEN total_nodes_completed + 1 
      ELSE total_nodes_completed 
    END,
    neural_level = CASE 
      WHEN (total_points + p_points) >= 1000 THEN 5
      WHEN (total_points + p_points) >= 700 THEN 4
      WHEN (total_points + p_points) >= 400 THEN 3
      WHEN (total_points + p_points) >= 200 THEN 2
      ELSE 1
    END,
    last_active_at = CURRENT_TIMESTAMP,
    updated_at = CURRENT_TIMESTAMP
  WHERE id = p_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function to get user progress summary
CREATE OR REPLACE FUNCTION get_user_progress_summary(p_user_id UUID)
RETURNS TABLE (
  total_nodes_completed INTEGER,
  total_points_earned INTEGER,
  average_quiz_score NUMERIC,
  total_time_spent INTEGER,
  recent_completions JSON
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    COUNT(*)::INTEGER as total_nodes_completed,
    COALESCE(SUM(points_earned), 0)::INTEGER as total_points_earned,
    ROUND(AVG(quiz_score), 2) as average_quiz_score,
    COALESCE(SUM(time_spent_seconds), 0)::INTEGER as total_time_spent,
    (
      SELECT JSON_AGG(
        JSON_BUILD_OBJECT(
          'node_id', node_id,
          'quiz_score', quiz_score,
          'points_earned', points_earned,
          'completed_at', completed_at
        )
      )
      FROM (
        SELECT node_id, quiz_score, points_earned, completed_at
        FROM user_progress
        WHERE user_id = p_user_id
        ORDER BY completed_at DESC
        LIMIT 10
      ) recent
    ) as recent_completions
  FROM user_progress
  WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function to check and award achievements
CREATE OR REPLACE FUNCTION check_and_award_achievements(p_user_id UUID)
RETURNS TABLE (
  new_achievements JSON
) AS $$
DECLARE
  v_total_points INTEGER;
  v_total_nodes INTEGER;
  v_perfect_quizzes INTEGER;
  v_achievement_id UUID;
  v_new_achievements JSON;
BEGIN
  -- Get user stats
  SELECT total_points, total_nodes_completed 
  INTO v_total_points, v_total_nodes
  FROM user_profiles 
  WHERE id = p_user_id;

  -- Count perfect quizzes
  SELECT COUNT(*) INTO v_perfect_quizzes
  FROM user_progress
  WHERE user_id = p_user_id AND quiz_score = 100;

  -- Check First Steps achievement (1 node completed)
  IF v_total_nodes >= 1 THEN
    SELECT id INTO v_achievement_id 
    FROM achievements 
    WHERE name = 'First Steps';
    
    INSERT INTO user_achievements (user_id, achievement_id)
    VALUES (p_user_id, v_achievement_id)
    ON CONFLICT (user_id, achievement_id) DO NOTHING;
  END IF;

  -- Check Quick Learner achievement (5 nodes completed)
  IF v_total_nodes >= 5 THEN
    SELECT id INTO v_achievement_id 
    FROM achievements 
    WHERE name = 'Quick Learner';
    
    INSERT INTO user_achievements (user_id, achievement_id)
    VALUES (p_user_id, v_achievement_id)
    ON CONFLICT (user_id, achievement_id) DO NOTHING;
  END IF;

  -- Check Knowledge Hunter achievement (500 points)
  IF v_total_points >= 500 THEN
    SELECT id INTO v_achievement_id 
    FROM achievements 
    WHERE name = 'Knowledge Hunter';
    
    INSERT INTO user_achievements (user_id, achievement_id)
    VALUES (p_user_id, v_achievement_id)
    ON CONFLICT (user_id, achievement_id) DO NOTHING;
  END IF;

  -- Check Perfectionist achievement (10 perfect quizzes)
  IF v_perfect_quizzes >= 10 THEN
    SELECT id INTO v_achievement_id 
    FROM achievements 
    WHERE name = 'Perfectionist';
    
    INSERT INTO user_achievements (user_id, achievement_id)
    VALUES (p_user_id, v_achievement_id)
    ON CONFLICT (user_id, achievement_id) DO NOTHING;
  END IF;

  -- Return newly earned achievements
  SELECT JSON_AGG(
    JSON_BUILD_OBJECT(
      'name', a.name,
      'description', a.description,
      'icon_name', a.icon_name,
      'earned_at', ua.earned_at
    )
  ) INTO v_new_achievements
  FROM user_achievements ua
  JOIN achievements a ON ua.achievement_id = a.id
  WHERE ua.user_id = p_user_id
    AND ua.earned_at >= NOW() - INTERVAL '1 minute';

  RETURN QUERY SELECT v_new_achievements;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function to get leaderboard
CREATE OR REPLACE FUNCTION get_leaderboard(p_limit INTEGER DEFAULT 10)
RETURNS TABLE (
  user_id UUID,
  username VARCHAR(50),
  display_name VARCHAR(100),
  avatar_url TEXT,
  total_points INTEGER,
  neural_level INTEGER,
  total_nodes_completed INTEGER,
  rank BIGINT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    up.id as user_id,
    up.username,
    up.display_name,
    up.avatar_url,
    up.total_points,
    up.neural_level,
    up.total_nodes_completed,
    ROW_NUMBER() OVER (ORDER BY up.total_points DESC) as rank
  FROM user_profiles up
  ORDER BY up.total_points DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permissions
GRANT EXECUTE ON FUNCTION update_user_stats TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_progress_summary TO authenticated;
GRANT EXECUTE ON FUNCTION check_and_award_achievements TO authenticated;
GRANT EXECUTE ON FUNCTION get_leaderboard TO public;

-- ================================================
-- Verification
-- ================================================

DO $$
BEGIN
  RAISE NOTICE 'Progress functions created successfully!';
  RAISE NOTICE 'Functions created:';
  RAISE NOTICE '  - update_user_stats';
  RAISE NOTICE '  - get_user_progress_summary';
  RAISE NOTICE '  - check_and_award_achievements';
  RAISE NOTICE '  - get_leaderboard';
END $$;