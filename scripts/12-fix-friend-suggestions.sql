-- Drop existing view if it exists
DROP VIEW IF EXISTS friend_suggestions;

-- Create or replace the get_friend_suggestions function
CREATE OR REPLACE FUNCTION get_friend_suggestions(p_user_id UUID)
RETURNS TABLE (
  suggested_user_id UUID,
  username VARCHAR(50),
  neural_level INTEGER,
  total_points INTEGER,
  common_groups BIGINT,
  common_nodes BIGINT
) 
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
  WITH user_friends AS (
    -- Get all existing friends
    SELECT friend_id 
    FROM friends 
    WHERE user_id = p_user_id
  ),
  friend_requests_sent AS (
    -- Get all pending friend requests sent by user
    SELECT receiver_id 
    FROM friend_requests 
    WHERE sender_id = p_user_id 
      AND status IN ('pending', 'accepted')
  ),
  friend_requests_received AS (
    -- Get all pending friend requests received by user
    SELECT sender_id 
    FROM friend_requests 
    WHERE receiver_id = p_user_id 
      AND status IN ('pending', 'accepted')
  ),
  excluded_users AS (
    -- Combine all users to exclude
    SELECT friend_id AS user_id FROM user_friends
    UNION
    SELECT receiver_id AS user_id FROM friend_requests_sent
    UNION
    SELECT sender_id AS user_id FROM friend_requests_received
    UNION
    SELECT p_user_id AS user_id -- Exclude self
  ),
  eligible_users AS (
    -- Get all users not in excluded list
    SELECT DISTINCT p.id, p.username, p.neural_level, p.total_points
    FROM user_profiles p
    WHERE p.id NOT IN (SELECT user_id FROM excluded_users)
      AND p.id IS NOT NULL
  ),
  common_study_groups AS (
    -- Count common study groups
    SELECT 
      eu.id AS user_id,
      COUNT(DISTINCT sgm2.group_id) AS common_groups
    FROM eligible_users eu
    LEFT JOIN study_group_members sgm1 ON sgm1.user_id = p_user_id
    LEFT JOIN study_group_members sgm2 ON sgm2.user_id = eu.id 
      AND sgm2.group_id = sgm1.group_id
    GROUP BY eu.id
  ),
  common_progress AS (
    -- Count common knowledge nodes
    SELECT 
      eu.id AS user_id,
      COUNT(DISTINCT up2.knowledge_node_id) AS common_nodes
    FROM eligible_users eu
    LEFT JOIN user_progress up1 ON up1.user_id = p_user_id
    LEFT JOIN user_progress up2 ON up2.user_id = eu.id 
      AND up2.knowledge_node_id = up1.knowledge_node_id
    GROUP BY eu.id
  )
  SELECT 
    eu.id AS suggested_user_id,
    eu.username,
    eu.neural_level,
    eu.total_points,
    COALESCE(csg.common_groups, 0) AS common_groups,
    COALESCE(cp.common_nodes, 0) AS common_nodes
  FROM eligible_users eu
  LEFT JOIN common_study_groups csg ON csg.user_id = eu.id
  LEFT JOIN common_progress cp ON cp.user_id = eu.id
  ORDER BY 
    COALESCE(csg.common_groups, 0) DESC,
    COALESCE(cp.common_nodes, 0) DESC,
    eu.neural_level DESC,
    eu.total_points DESC
  LIMIT 10;
END;
$$;

-- Grant execute permission to authenticated users
GRANT EXECUTE ON FUNCTION get_friend_suggestions(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_friend_suggestions(UUID) TO anon;

-- Create a simple view for testing (optional)
CREATE OR REPLACE VIEW all_user_profiles AS
SELECT 
  id,
  username,
  neural_level,
  total_points,
  created_at
FROM user_profiles
WHERE username IS NOT NULL;

-- Grant select permission on the view
GRANT SELECT ON all_user_profiles TO authenticated;
GRANT SELECT ON all_user_profiles TO anon;