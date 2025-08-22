-- Remove has_learning_content field from skill_tree_nodes table
-- Created: 2025-08-22
-- Updated: 2025-08-22 to handle view dependency
-- Purpose: Clean up database schema by removing redundant has_learning_content field

-- First, let's create a backup
CREATE TABLE skill_tree_nodes_bkp_20250822 AS SELECT * FROM skill_tree_nodes;

-- Check current structure before change
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'skill_tree_nodes' 
ORDER BY ordinal_position;

-- Step 1: Get the current view definition to recreate it
SELECT definition FROM pg_views WHERE viewname = 'skill_nodes_with_content_and_questions';

-- Step 2: Drop the dependent view first
DROP VIEW IF EXISTS skill_nodes_with_content_and_questions;

-- Step 3: Remove the has_learning_content column
ALTER TABLE skill_tree_nodes DROP COLUMN IF EXISTS has_learning_content;

-- Step 4: Recreate the view without has_learning_content
-- This view will be recreated based on learning_content_ids instead
CREATE OR REPLACE VIEW skill_nodes_with_content_and_questions AS
SELECT 
    stn.id,
    stn.parent_id,
    stn.name,
    stn.learning_content_ids,
    stn.created_at,
    stn.updated_at,
    CASE 
        WHEN stn.learning_content_ids IS NOT NULL AND array_length(stn.learning_content_ids, 1) > 0 
        THEN array_length(stn.learning_content_ids, 1)
        ELSE 0 
    END as content_count,
    0 as question_count,  -- Questions are not directly linked to skill nodes
    EXISTS(
        SELECT 1 
        FROM skill_tree_nodes child 
        WHERE child.parent_id = stn.id
    ) as has_children
FROM skill_tree_nodes stn;

-- Verify the field has been removed
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'skill_tree_nodes' 
ORDER BY ordinal_position;

-- Confirm we still have all records
SELECT COUNT(*) as total_records FROM skill_tree_nodes;

-- Test the recreated view
SELECT * FROM skill_nodes_with_content_and_questions LIMIT 5;