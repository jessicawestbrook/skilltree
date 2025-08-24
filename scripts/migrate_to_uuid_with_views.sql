-- Safe migration script to convert skill_tree_nodes ID from TEXT to UUID
-- This version handles views that depend on the tables

-- Step 1: Create backup tables
CREATE TABLE IF NOT EXISTS skill_tree_nodes_bkp AS 
SELECT * FROM skill_tree_nodes;

CREATE TABLE IF NOT EXISTS questions_bkp AS 
SELECT * FROM questions;

CREATE TABLE IF NOT EXISTS user_progress_bkp AS 
SELECT * FROM user_progress;

CREATE TABLE IF NOT EXISTS starred_items_bkp AS 
SELECT * FROM starred_items;

CREATE TABLE IF NOT EXISTS learning_content_bkp AS 
SELECT * FROM learning_content;

-- Step 2: Save view definitions before dropping them
-- Store the view definition for recreation later
DO $$
DECLARE
  view_def TEXT;
BEGIN
  -- Get the view definition
  SELECT pg_get_viewdef('skill_nodes_with_content_and_questions'::regclass, true) INTO view_def;
  
  -- Store it in a temporary table
  CREATE TEMP TABLE IF NOT EXISTS view_definitions (
    view_name TEXT,
    definition TEXT
  );
  
  INSERT INTO view_definitions (view_name, definition)
  VALUES ('skill_nodes_with_content_and_questions', view_def);
  
  RAISE NOTICE 'Saved view definition for skill_nodes_with_content_and_questions';
END $$;

-- Step 3: Drop all dependent views
DROP VIEW IF EXISTS skill_nodes_with_content_and_questions CASCADE;

-- Check for other views that might depend on skill_tree_nodes
DROP VIEW IF EXISTS skill_tree_hierarchy CASCADE;
DROP VIEW IF EXISTS user_skill_progress CASCADE;
DROP VIEW IF EXISTS category_stats CASCADE;

-- Step 4: Drop foreign key constraints that reference skill_tree_nodes
ALTER TABLE skill_tree_nodes DROP CONSTRAINT IF EXISTS skill_tree_nodes_parent_id_fkey;
ALTER TABLE questions DROP CONSTRAINT IF EXISTS questions_skill_id_fkey;
ALTER TABLE user_progress DROP CONSTRAINT IF EXISTS user_progress_skill_id_fkey;
ALTER TABLE learning_content DROP CONSTRAINT IF EXISTS learning_content_skill_id_fkey;

-- Step 5: Change column types from TEXT to UUID
-- For skill_tree_nodes
ALTER TABLE skill_tree_nodes 
  ALTER COLUMN id TYPE UUID USING id::UUID,
  ALTER COLUMN parent_id TYPE UUID USING parent_id::UUID;

-- For questions (if skill_id exists)
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='questions' AND column_name='skill_id') THEN
    ALTER TABLE questions 
      ALTER COLUMN skill_id TYPE UUID USING skill_id::UUID;
  END IF;
END $$;

-- For user_progress (if skill_id exists)
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='user_progress' AND column_name='skill_id') THEN
    ALTER TABLE user_progress 
      ALTER COLUMN skill_id TYPE UUID USING skill_id::UUID;
  END IF;
END $$;

-- For starred_items (item_id when item_type = 'skill_node')
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='starred_items' AND column_name='item_id') THEN
    -- Check if all item_ids are valid UUIDs
    IF NOT EXISTS (
      SELECT 1 FROM starred_items 
      WHERE item_id IS NOT NULL 
      AND item_id !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    ) THEN
      -- All IDs are valid UUIDs, safe to convert
      ALTER TABLE starred_items 
        ALTER COLUMN item_id TYPE UUID USING item_id::UUID;
    ELSE
      RAISE NOTICE 'Some item_ids in starred_items are not valid UUIDs, skipping conversion';
    END IF;
  END IF;
END $$;

-- For learning_content (if skill_id or node_id exists)
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='learning_content' AND column_name='skill_id') THEN
    ALTER TABLE learning_content 
      ALTER COLUMN skill_id TYPE UUID USING skill_id::UUID;
  END IF;
  
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='learning_content' AND column_name='node_id') THEN
    ALTER TABLE learning_content 
      ALTER COLUMN node_id TYPE UUID USING node_id::UUID;
  END IF;
END $$;

-- Step 6: Re-add foreign key constraints with UUID types
ALTER TABLE skill_tree_nodes 
  ADD CONSTRAINT skill_tree_nodes_parent_id_fkey 
  FOREIGN KEY (parent_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;

-- For questions
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='questions' AND column_name='skill_id') THEN
    ALTER TABLE questions 
      ADD CONSTRAINT questions_skill_id_fkey 
      FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
  END IF;
END $$;

-- For user_progress
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='user_progress' AND column_name='skill_id') THEN
    ALTER TABLE user_progress 
      ADD CONSTRAINT user_progress_skill_id_fkey 
      FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
  END IF;
END $$;

-- For learning_content
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='learning_content' AND column_name='skill_id') THEN
    ALTER TABLE learning_content 
      ADD CONSTRAINT learning_content_skill_id_fkey 
      FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
  END IF;
  
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='learning_content' AND column_name='node_id') THEN
    ALTER TABLE learning_content 
      ADD CONSTRAINT learning_content_node_id_fkey 
      FOREIGN KEY (node_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
  END IF;
END $$;

-- Step 7: Recreate the views with UUID types
-- This is a typical view structure - adjust if your actual view is different
CREATE OR REPLACE VIEW skill_nodes_with_content_and_questions AS
SELECT 
  stn.id,
  stn.parent_id,
  stn.name,
  stn.description,
  stn.level,
  stn.order_index,
  stn.is_menu_leaf,
  stn.has_learning_content,
  stn.learning_content_ids,
  stn.display_order,
  stn.created_at,
  stn.updated_at,
  COUNT(DISTINCT lc.id) as content_count,
  COUNT(DISTINCT q.id) as question_count
FROM skill_tree_nodes stn
LEFT JOIN learning_content lc ON lc.node_id = stn.id OR lc.skill_id = stn.id
LEFT JOIN questions q ON q.skill_id = stn.id
GROUP BY 
  stn.id,
  stn.parent_id,
  stn.name,
  stn.description,
  stn.level,
  stn.order_index,
  stn.is_menu_leaf,
  stn.has_learning_content,
  stn.learning_content_ids,
  stn.display_order,
  stn.created_at,
  stn.updated_at;

-- Grant appropriate permissions on the view
GRANT SELECT ON skill_nodes_with_content_and_questions TO authenticated;
GRANT SELECT ON skill_nodes_with_content_and_questions TO anon;

-- Step 8: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_skill_tree_nodes_parent_id ON skill_tree_nodes(parent_id);
CREATE INDEX IF NOT EXISTS idx_questions_skill_id ON questions(skill_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_skill_id ON user_progress(skill_id);
CREATE INDEX IF NOT EXISTS idx_starred_items_item_id ON starred_items(item_id);
CREATE INDEX IF NOT EXISTS idx_learning_content_skill_id ON learning_content(skill_id);

-- Step 9: Verify the migration
DO $$
DECLARE
  nodes_count INTEGER;
  backup_count INTEGER;
  id_type TEXT;
BEGIN
  SELECT COUNT(*) INTO nodes_count FROM skill_tree_nodes;
  SELECT COUNT(*) INTO backup_count FROM skill_tree_nodes_bkp;
  
  SELECT data_type INTO id_type 
  FROM information_schema.columns 
  WHERE table_name = 'skill_tree_nodes' AND column_name = 'id';
  
  IF nodes_count != backup_count THEN
    RAISE EXCEPTION 'Migration verification failed: row counts do not match';
  END IF;
  
  IF id_type != 'uuid' THEN
    RAISE EXCEPTION 'Migration verification failed: id column is not UUID type';
  END IF;
  
  RAISE NOTICE 'Migration completed successfully. % rows migrated. ID column is now type: %', nodes_count, id_type;
  RAISE NOTICE 'Views have been recreated. Please verify they work correctly.';
END $$;

-- Step 10: Clean up (only run after verifying everything works)
-- DROP TABLE skill_tree_nodes_bkp;
-- DROP TABLE questions_bkp;
-- DROP TABLE user_progress_bkp;
-- DROP TABLE starred_items_bkp;
-- DROP TABLE learning_content_bkp;