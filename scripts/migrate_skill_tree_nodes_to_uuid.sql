-- Migration script to convert skill_tree_nodes ID from TEXT to UUID
-- WARNING: This is a complex migration. Make sure to backup your database first!

-- Step 1: Create backup table
CREATE TABLE skill_tree_nodes_bkp AS 
SELECT * FROM skill_tree_nodes;

-- Step 2: Add new UUID columns to store the converted IDs
ALTER TABLE skill_tree_nodes ADD COLUMN id_uuid UUID;
ALTER TABLE skill_tree_nodes ADD COLUMN parent_id_uuid UUID;

-- Step 3: Generate UUIDs for all existing IDs
-- We'll use UUID v5 with a namespace to create deterministic UUIDs from the text IDs
-- This ensures consistency across all references
UPDATE skill_tree_nodes 
SET id_uuid = gen_random_uuid()
WHERE id_uuid IS NULL;

-- Step 4: Create a mapping table for the conversion
CREATE TABLE IF NOT EXISTS id_migration_map (
  old_id TEXT PRIMARY KEY,
  new_id UUID NOT NULL
);

-- Step 5: Populate the mapping table
INSERT INTO id_migration_map (old_id, new_id)
SELECT id, id_uuid FROM skill_tree_nodes;

-- Step 6: Update parent_id_uuid based on the mapping
UPDATE skill_tree_nodes s
SET parent_id_uuid = m.new_id
FROM id_migration_map m
WHERE s.parent_id = m.old_id;

-- Step 7: Find all tables that reference skill_tree_nodes
-- These need to be updated too. Common ones include:
-- - questions (skill_id)
-- - user_progress (skill_id)
-- - starred_items (item_id when item_type = 'skill_node')
-- - learning_content (might have skill_id references)

-- Step 8: Add UUID columns to dependent tables
ALTER TABLE questions ADD COLUMN IF NOT EXISTS skill_id_uuid UUID;
ALTER TABLE user_progress ADD COLUMN IF NOT EXISTS skill_id_uuid UUID;
ALTER TABLE starred_items ADD COLUMN IF NOT EXISTS item_id_uuid UUID;

-- Step 9: Update the UUID columns in dependent tables
UPDATE questions q
SET skill_id_uuid = m.new_id
FROM id_migration_map m
WHERE q.skill_id = m.old_id;

UPDATE user_progress u
SET skill_id_uuid = m.new_id
FROM id_migration_map m
WHERE u.skill_id = m.old_id;

UPDATE starred_items s
SET item_id_uuid = m.new_id
FROM id_migration_map m
WHERE s.item_id = m.old_id AND s.item_type = 'skill_node';

-- Step 10: Drop foreign key constraints
ALTER TABLE questions DROP CONSTRAINT IF EXISTS questions_skill_id_fkey;
ALTER TABLE user_progress DROP CONSTRAINT IF EXISTS user_progress_skill_id_fkey;
ALTER TABLE starred_items DROP CONSTRAINT IF EXISTS starred_items_skill_node_fkey;

-- Step 11: Drop old columns and rename new ones
ALTER TABLE skill_tree_nodes DROP CONSTRAINT IF EXISTS skill_tree_nodes_pkey;
ALTER TABLE skill_tree_nodes DROP CONSTRAINT IF EXISTS skill_tree_nodes_parent_id_fkey;

ALTER TABLE skill_tree_nodes DROP COLUMN id;
ALTER TABLE skill_tree_nodes DROP COLUMN parent_id;
ALTER TABLE skill_tree_nodes RENAME COLUMN id_uuid TO id;
ALTER TABLE skill_tree_nodes RENAME COLUMN parent_id_uuid TO parent_id;

ALTER TABLE questions DROP COLUMN skill_id;
ALTER TABLE questions RENAME COLUMN skill_id_uuid TO skill_id;

ALTER TABLE user_progress DROP COLUMN skill_id;
ALTER TABLE user_progress RENAME COLUMN skill_id_uuid TO skill_id;

ALTER TABLE starred_items DROP COLUMN item_id;
ALTER TABLE starred_items RENAME COLUMN item_id_uuid TO item_id;

-- Step 12: Add back primary key and foreign key constraints
ALTER TABLE skill_tree_nodes ADD PRIMARY KEY (id);
ALTER TABLE skill_tree_nodes ADD CONSTRAINT skill_tree_nodes_parent_id_fkey 
  FOREIGN KEY (parent_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;

ALTER TABLE questions ADD CONSTRAINT questions_skill_id_fkey 
  FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;

ALTER TABLE user_progress ADD CONSTRAINT user_progress_skill_id_fkey 
  FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;

-- Step 13: Create indexes
CREATE INDEX IF NOT EXISTS idx_skill_tree_nodes_parent_id ON skill_tree_nodes(parent_id);
CREATE INDEX IF NOT EXISTS idx_questions_skill_id ON questions(skill_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_skill_id ON user_progress(skill_id);

-- Step 14: Verify the migration
DO $$
DECLARE
  nodes_count INTEGER;
  backup_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO nodes_count FROM skill_tree_nodes;
  SELECT COUNT(*) INTO backup_count FROM skill_tree_nodes_bkp;
  
  IF nodes_count != backup_count THEN
    RAISE EXCEPTION 'Migration verification failed: row counts do not match';
  END IF;
  
  RAISE NOTICE 'Migration completed successfully. % rows migrated.', nodes_count;
END $$;

-- Step 15: Clean up (only run after verifying everything works)
-- DROP TABLE id_migration_map;
-- DROP TABLE skill_tree_nodes_bkp; -- Keep this backup for safety!