-- Script to add Money Counting to user's recent activity
-- Run this in Supabase SQL editor

-- First, find the Money Counting node ID
WITH money_counting_node AS (
  SELECT id, name, learning_area
  FROM skill_tree_nodes
  WHERE LOWER(name) LIKE '%money counting%'
  LIMIT 1
)
-- Insert a user_progress record for Money Counting
INSERT INTO user_progress (
  user_id,
  skill_id,
  status,
  rating,
  last_accessed,
  created_at,
  updated_at
)
SELECT 
  auth.uid() as user_id,  -- This will use the currently logged-in user
  mc.id as skill_id,
  'in_progress' as status,  -- or 'completed' if you've finished it
  0 as rating,  -- Set to a value 0-100 if completed
  NOW() as last_accessed,
  NOW() as created_at,
  NOW() as updated_at
FROM money_counting_node mc
WHERE NOT EXISTS (
  -- Only insert if there's no existing progress for this node
  SELECT 1 
  FROM user_progress 
  WHERE user_id = auth.uid() 
  AND skill_id = mc.id
);

-- Verify the insertion
SELECT 
  up.*,
  stn.name as node_name,
  stn.learning_area
FROM user_progress up
JOIN skill_tree_nodes stn ON up.skill_id = stn.id
WHERE up.user_id = auth.uid()
AND LOWER(stn.name) LIKE '%money%'
ORDER BY up.last_accessed DESC;