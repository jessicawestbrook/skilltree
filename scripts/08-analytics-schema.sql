-- ================================================
-- ANALYTICS AND INSIGHTS SCHEMA
-- ================================================
-- Tables and functions for learning analytics
-- ================================================

-- Create learning_sessions table to track detailed session data
CREATE TABLE IF NOT EXISTS learning_sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  session_start TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  session_end TIMESTAMP WITH TIME ZONE,
  total_duration_seconds INTEGER DEFAULT 0,
  nodes_attempted JSONB DEFAULT '[]'::jsonb,
  nodes_completed JSONB DEFAULT '[]'::jsonb,
  total_questions_answered INTEGER DEFAULT 0,
  correct_answers INTEGER DEFAULT 0,
  user_agent TEXT,
  device_type VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_learning_sessions_user_id ON learning_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_start ON learning_sessions(session_start);

-- Create learning_analytics table for detailed interaction tracking
CREATE TABLE IF NOT EXISTS learning_analytics (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  session_id UUID REFERENCES learning_sessions(id) ON DELETE CASCADE,
  event_type VARCHAR(50) NOT NULL, -- 'quiz_start', 'quiz_complete', 'node_visit', 'content_view', etc.
  node_id VARCHAR(255) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  event_data JSONB DEFAULT '{}'::jsonb,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_learning_analytics_user_id ON learning_analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_analytics_session_id ON learning_analytics(session_id);
CREATE INDEX IF NOT EXISTS idx_learning_analytics_event_type ON learning_analytics(event_type);
CREATE INDEX IF NOT EXISTS idx_learning_analytics_timestamp ON learning_analytics(timestamp);

-- Create weekly_insights table for aggregated insights
CREATE TABLE IF NOT EXISTS weekly_insights (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  week_start DATE NOT NULL,
  total_study_time_minutes INTEGER DEFAULT 0,
  nodes_completed INTEGER DEFAULT 0,
  quiz_accuracy DECIMAL(5,2) DEFAULT 0,
  streak_days INTEGER DEFAULT 0,
  most_studied_domain VARCHAR(100),
  improvement_areas JSONB DEFAULT '[]'::jsonb,
  achievements_earned JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, week_start)
);

CREATE INDEX IF NOT EXISTS idx_weekly_insights_user_id ON weekly_insights(user_id);
CREATE INDEX IF NOT EXISTS idx_weekly_insights_week_start ON weekly_insights(week_start);

-- Create learning_recommendations table
CREATE TABLE IF NOT EXISTS learning_recommendations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  recommendation_type VARCHAR(50) NOT NULL, -- 'next_node', 'review', 'challenge', 'weak_area'
  node_id VARCHAR(255) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  priority_score INTEGER DEFAULT 50, -- 1-100
  reasoning TEXT,
  is_active BOOLEAN DEFAULT true,
  expires_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_learning_recommendations_user_id ON learning_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_recommendations_active ON learning_recommendations(is_active);

-- Enable RLS
ALTER TABLE learning_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE weekly_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_recommendations ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can manage own learning sessions" ON learning_sessions
  FOR ALL TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can manage own analytics" ON learning_analytics
  FOR ALL TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own insights" ON weekly_insights
  FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own recommendations" ON learning_recommendations
  FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

-- ================================================
-- ANALYTICS FUNCTIONS
-- ================================================

-- Function to start a learning session
CREATE OR REPLACE FUNCTION start_learning_session(
  p_user_id UUID,
  p_user_agent TEXT DEFAULT NULL,
  p_device_type VARCHAR(50) DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
  v_session_id UUID;
BEGIN
  INSERT INTO learning_sessions (user_id, user_agent, device_type)
  VALUES (p_user_id, p_user_agent, p_device_type)
  RETURNING id INTO v_session_id;
  
  RETURN v_session_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to end a learning session
CREATE OR REPLACE FUNCTION end_learning_session(
  p_session_id UUID,
  p_total_duration_seconds INTEGER DEFAULT NULL
)
RETURNS void AS $$
BEGIN
  UPDATE learning_sessions
  SET 
    session_end = CURRENT_TIMESTAMP,
    total_duration_seconds = COALESCE(p_total_duration_seconds, 
      EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - session_start))::INTEGER)
  WHERE id = p_session_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to track learning events
CREATE OR REPLACE FUNCTION track_learning_event(
  p_user_id UUID,
  p_event_type VARCHAR(50),
  p_session_id UUID DEFAULT NULL,
  p_node_id VARCHAR(255) DEFAULT NULL,
  p_event_data JSONB DEFAULT '{}'::jsonb
)
RETURNS void AS $$
BEGIN
  INSERT INTO learning_analytics (user_id, session_id, event_type, node_id, event_data)
  VALUES (p_user_id, p_session_id, p_event_type, p_node_id, p_event_data);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get user learning analytics
CREATE OR REPLACE FUNCTION get_user_analytics(
  p_user_id UUID,
  p_days_back INTEGER DEFAULT 30
)
RETURNS TABLE (
  total_study_time_hours DECIMAL,
  nodes_completed INTEGER,
  average_quiz_score DECIMAL,
  study_streak_days INTEGER,
  most_active_domains JSON,
  daily_activity JSON,
  quiz_performance_trend JSON
) AS $$
BEGIN
  RETURN QUERY
  WITH study_time AS (
    SELECT COALESCE(SUM(total_duration_seconds), 0)::DECIMAL / 3600 as hours
    FROM learning_sessions 
    WHERE user_id = p_user_id 
      AND session_start >= CURRENT_DATE - INTERVAL '1 day' * p_days_back
  ),
  completed_nodes AS (
    SELECT COUNT(DISTINCT node_id)::INTEGER as count
    FROM user_progress 
    WHERE user_id = p_user_id
      AND completed_at >= CURRENT_DATE - INTERVAL '1 day' * p_days_back
  ),
  avg_quiz_score AS (
    SELECT COALESCE(AVG(quiz_score), 0)::DECIMAL as score
    FROM user_progress 
    WHERE user_id = p_user_id
      AND completed_at >= CURRENT_DATE - INTERVAL '1 day' * p_days_back
  ),
  streak AS (
    SELECT COUNT(DISTINCT DATE(session_start))::INTEGER as days
    FROM learning_sessions
    WHERE user_id = p_user_id
      AND session_start >= CURRENT_DATE - INTERVAL '1 day' * 7
  ),
  domains AS (
    SELECT JSON_AGG(
      JSON_BUILD_OBJECT(
        'domain', kn.domain,
        'count', COUNT(*)
      ) ORDER BY COUNT(*) DESC
    ) as domain_data
    FROM user_progress up
    JOIN knowledge_nodes kn ON up.node_id = kn.id
    WHERE up.user_id = p_user_id
      AND up.completed_at >= CURRENT_DATE - INTERVAL '1 day' * p_days_back
    GROUP BY kn.domain
    LIMIT 5
  ),
  daily AS (
    SELECT JSON_AGG(
      JSON_BUILD_OBJECT(
        'date', date,
        'study_time_minutes', study_time_minutes,
        'nodes_completed', nodes_completed
      ) ORDER BY date
    ) as daily_data
    FROM (
      SELECT 
        DATE(COALESCE(ls.session_start, up.completed_at)) as date,
        COALESCE(SUM(ls.total_duration_seconds), 0) / 60 as study_time_minutes,
        COUNT(DISTINCT up.node_id) as nodes_completed
      FROM learning_sessions ls
      FULL OUTER JOIN user_progress up ON DATE(ls.session_start) = DATE(up.completed_at) 
        AND ls.user_id = up.user_id
      WHERE COALESCE(ls.user_id, up.user_id) = p_user_id
        AND DATE(COALESCE(ls.session_start, up.completed_at)) >= CURRENT_DATE - INTERVAL '1 day' * p_days_back
      GROUP BY DATE(COALESCE(ls.session_start, up.completed_at))
      ORDER BY date DESC
      LIMIT p_days_back
    ) daily_stats
  ),
  quiz_trend AS (
    SELECT JSON_AGG(
      JSON_BUILD_OBJECT(
        'date', date,
        'average_score', avg_score
      ) ORDER BY date
    ) as trend_data
    FROM (
      SELECT 
        DATE(completed_at) as date,
        AVG(quiz_score) as avg_score
      FROM user_progress
      WHERE user_id = p_user_id
        AND completed_at >= CURRENT_DATE - INTERVAL '1 day' * p_days_back
      GROUP BY DATE(completed_at)
      ORDER BY date DESC
      LIMIT 14
    ) trend_stats
  )
  SELECT 
    st.hours,
    cn.count,
    aq.score,
    s.days,
    COALESCE(d.domain_data, '[]'::json),
    COALESCE(da.daily_data, '[]'::json),
    COALESCE(qt.trend_data, '[]'::json)
  FROM study_time st
  CROSS JOIN completed_nodes cn
  CROSS JOIN avg_quiz_score aq
  CROSS JOIN streak s
  CROSS JOIN domains d
  CROSS JOIN daily da
  CROSS JOIN quiz_trend qt;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to generate learning insights
CREATE OR REPLACE FUNCTION generate_learning_insights(p_user_id UUID)
RETURNS TABLE (
  insight_type VARCHAR(50),
  title TEXT,
  description TEXT,
  action_suggestion TEXT,
  priority INTEGER
) AS $$
DECLARE
  v_avg_score DECIMAL;
  v_total_nodes INTEGER;
  v_recent_activity INTEGER;
  v_weak_domains TEXT[];
BEGIN
  -- Get user stats
  SELECT AVG(quiz_score), COUNT(*) 
  INTO v_avg_score, v_total_nodes
  FROM user_progress 
  WHERE user_id = p_user_id;
  
  -- Check recent activity
  SELECT COUNT(*)
  INTO v_recent_activity
  FROM learning_sessions
  WHERE user_id = p_user_id 
    AND session_start >= CURRENT_DATE - INTERVAL '7 days';
  
  -- Find weak domains (below 70% average)
  SELECT ARRAY_AGG(kn.domain)
  INTO v_weak_domains
  FROM (
    SELECT kn.domain, AVG(up.quiz_score) as avg_score
    FROM user_progress up
    JOIN knowledge_nodes kn ON up.node_id = kn.id
    WHERE up.user_id = p_user_id
    GROUP BY kn.domain
    HAVING AVG(up.quiz_score) < 70
  ) weak_domains_query;
  
  -- Generate insights based on patterns
  
  -- Low quiz performance insight
  IF v_avg_score < 70 THEN
    RETURN QUERY SELECT 
      'performance'::VARCHAR(50),
      'Improve Quiz Performance'::TEXT,
      'Your average quiz score is below 70%. Consider reviewing content before taking quizzes.'::TEXT,
      'Review course materials more thoroughly before attempting quizzes'::TEXT,
      90;
  END IF;
  
  -- Inactivity insight
  IF v_recent_activity = 0 THEN
    RETURN QUERY SELECT 
      'engagement'::VARCHAR(50),
      'Stay Consistent'::TEXT,
      'You haven''t studied in the past week. Consistency is key to effective learning.'::TEXT,
      'Set aside 15 minutes daily for learning to build a strong habit'::TEXT,
      95;
  END IF;
  
  -- Domain weakness insight
  IF array_length(v_weak_domains, 1) > 0 THEN
    RETURN QUERY SELECT 
      'weak_areas'::VARCHAR(50),
      'Focus on Weak Areas'::TEXT,
      'You have some domains where your performance could improve: ' || array_to_string(v_weak_domains, ', ')::TEXT,
      'Spend extra time reviewing these topics and retake related quizzes'::TEXT,
      80;
  END IF;
  
  -- Progress celebration
  IF v_total_nodes >= 10 AND v_avg_score >= 80 THEN
    RETURN QUERY SELECT 
      'achievement'::VARCHAR(50),
      'Excellent Progress!'::TEXT,
      'You''ve completed ' || v_total_nodes || ' nodes with an average score of ' || ROUND(v_avg_score, 1) || '%!'::TEXT,
      'Keep up the great work and consider tackling more challenging topics'::TEXT,
      70;
  END IF;
  
  RETURN;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to generate personalized recommendations
CREATE OR REPLACE FUNCTION generate_recommendations(p_user_id UUID)
RETURNS void AS $$
DECLARE
  v_user_level INTEGER;
  v_completed_nodes TEXT[];
  v_weak_domains TEXT[];
  rec RECORD;
BEGIN
  -- Clear old recommendations
  DELETE FROM learning_recommendations 
  WHERE user_id = p_user_id AND created_at < CURRENT_TIMESTAMP - INTERVAL '1 week';
  
  -- Get user data
  SELECT neural_level INTO v_user_level
  FROM user_profiles WHERE id = p_user_id;
  
  SELECT ARRAY_AGG(node_id) INTO v_completed_nodes
  FROM user_progress WHERE user_id = p_user_id;
  
  -- Find weak domains for review recommendations
  SELECT ARRAY_AGG(domain) INTO v_weak_domains
  FROM (
    SELECT kn.domain
    FROM user_progress up
    JOIN knowledge_nodes kn ON up.node_id = kn.id
    WHERE up.user_id = p_user_id AND up.quiz_score < 70
    GROUP BY kn.domain
  ) weak_domains_query;
  
  -- Generate next node recommendations
  FOR rec IN 
    SELECT kn.id, kn.name, kn.difficulty, kn.domain
    FROM knowledge_nodes kn
    WHERE kn.id NOT IN (SELECT UNNEST(COALESCE(v_completed_nodes, ARRAY[]::TEXT[])))
      AND NOT EXISTS (
        SELECT 1 FROM node_prerequisites np 
        WHERE np.node_id = kn.id 
          AND np.prerequisite_id NOT IN (SELECT UNNEST(COALESCE(v_completed_nodes, ARRAY[]::TEXT[])))
      )
    ORDER BY 
      CASE WHEN kn.difficulty = 'beginner' THEN 1
           WHEN kn.difficulty = 'intermediate' THEN 2
           ELSE 3 END,
      RANDOM()
    LIMIT 5
  LOOP
    INSERT INTO learning_recommendations (
      user_id, recommendation_type, node_id, priority_score, reasoning
    ) VALUES (
      p_user_id, 'next_node', rec.id, 85,
      'Perfect next step based on your current level and completed prerequisites'
    );
  END LOOP;
  
  -- Generate review recommendations for weak areas
  IF array_length(v_weak_domains, 1) > 0 THEN
    FOR rec IN
      SELECT kn.id, kn.name, kn.domain
      FROM knowledge_nodes kn
      JOIN user_progress up ON kn.id = up.node_id
      WHERE up.user_id = p_user_id 
        AND kn.domain = ANY(v_weak_domains)
        AND up.quiz_score < 70
      ORDER BY up.quiz_score ASC
      LIMIT 3
    LOOP
      INSERT INTO learning_recommendations (
        user_id, recommendation_type, node_id, priority_score, reasoning
      ) VALUES (
        p_user_id, 'review', rec.id, 75,
        'Review this topic to improve your understanding in ' || rec.domain
      );
    END LOOP;
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant permissions
GRANT EXECUTE ON FUNCTION start_learning_session TO authenticated;
GRANT EXECUTE ON FUNCTION end_learning_session TO authenticated;
GRANT EXECUTE ON FUNCTION track_learning_event TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_analytics TO authenticated;
GRANT EXECUTE ON FUNCTION generate_learning_insights TO authenticated;
GRANT EXECUTE ON FUNCTION generate_recommendations TO authenticated;

-- ================================================
-- Verification
-- ================================================

DO $$
BEGIN
  RAISE NOTICE 'Analytics schema created successfully!';
  RAISE NOTICE 'Tables created:';
  RAISE NOTICE '  - learning_sessions';
  RAISE NOTICE '  - learning_analytics';
  RAISE NOTICE '  - weekly_insights';
  RAISE NOTICE '  - learning_recommendations';
  RAISE NOTICE 'Functions created:';
  RAISE NOTICE '  - start_learning_session';
  RAISE NOTICE '  - end_learning_session';
  RAISE NOTICE '  - track_learning_event';
  RAISE NOTICE '  - get_user_analytics';
  RAISE NOTICE '  - generate_learning_insights';
  RAISE NOTICE '  - generate_recommendations';
END $$;