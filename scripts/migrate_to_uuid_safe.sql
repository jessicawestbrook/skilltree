-- Safe migration script to convert skill_tree_nodes ID from TEXT to UUID
-- This version only updates tables that exist in your database

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

-- Step 2: Check if IDs are already valid UUIDs (they appear to be)
-- Since your IDs like '460988d1-f216-48a5-a8cc-442bd6f55cd8' are already valid UUIDs,
-- we can simply change the column type

-- Step 3: Drop foreign key constraints that reference skill_tree_nodes
ALTER TABLE skill_tree_nodes DROP CONSTRAINT IF EXISTS skill_tree_nodes_parent_id_fkey;
ALTER TABLE questions DROP CONSTRAINT IF EXISTS questions_skill_id_fkey;
ALTER TABLE user_progress DROP CONSTRAINT IF EXISTS user_progress_skill_id_fkey;
ALTER TABLE learning_content DROP CONSTRAINT IF EXISTS learning_content_skill_id_fkey;

-- Step 4: Change column types from TEXT to UUID
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
-- This is trickier because item_id might contain different types
-- We'll only convert when item_type = 'skill_node'
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='starred_items' AND column_name='item_id') THEN
    -- First, check if all skill_node item_ids are valid UUIDs
    IF NOT EXISTS (
      SELECT 1 FROM starred_items 
      WHERE item_type = 'skill_node' 
      AND item_id !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    ) THEN
      -- All skill_node IDs are valid UUIDs, safe to convert
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

-- Step 5: Re-add foreign key constraints with UUID types
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

-- Step 6: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_skill_tree_nodes_parent_id ON skill_tree_nodes(parent_id);
CREATE INDEX IF NOT EXISTS idx_questions_skill_id ON questions(skill_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_skill_id ON user_progress(skill_id);
CREATE INDEX IF NOT EXISTS idx_starred_items_item_id ON starred_items(item_id);
CREATE INDEX IF NOT EXISTS idx_learning_content_skill_id ON learning_content(skill_id);

-- Step 7: Verify the migration
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
END $$;

-- Step 8: Now you can create the assessment_sessions table with proper UUID foreign keys
-- Run the create_assessment_sessions_table.sql script after this migration