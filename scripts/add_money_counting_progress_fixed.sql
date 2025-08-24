-- Script to add Money Counting to user's recent activity
-- Run this in Supabase SQL editor

-- First check the structure to understand the relationship
-- The skill_id appears to be an integer, so we need to find the right way to link it

-- Option 1: If there's a skills table with integer IDs
-- Check if there's a skills or learning_modules table
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE '%skill%' OR table_name LIKE '%learning%'
ORDER BY table_name;

-- Option 2: If skill_id directly references skill_tree_nodes somehow
-- Let's check what skill_id values already exist
SELECT DISTINCT 
    up.skill_id,
    stn.id as skill_id_ref,
    stn.name as skill_name
FROM user_progress up
LEFT JOIN skill_tree_nodes stn ON stn.id::text = up.skill_id::text
LIMIT 10;

-- Option 3: Manual insert with a specific skill_id
-- You may need to manually specify the skill_id for Money Counting
-- For example, if Money Counting has skill_id = 123:
/*
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
  auth.uid() as user_id,
  123 as skill_id,  -- Replace with actual skill_id for Money Counting
  'in_progress' as status,
  0 as rating,
  NOW() as last_accessed,
  NOW() as created_at,
  NOW() as updated_at
WHERE NOT EXISTS (
  SELECT 1 
  FROM user_progress 
  WHERE user_id = auth.uid() 
  AND skill_id = 123  -- Replace with actual skill_id
);
*/