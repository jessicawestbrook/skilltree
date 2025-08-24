-- Complete migration script to convert skill_tree_nodes ID from TEXT to UUID
-- This version handles ALL dependent tables and views dynamically

-- Step 1: Create comprehensive backups
CREATE TABLE IF NOT EXISTS skill_tree_nodes_bkp AS SELECT * FROM skill_tree_nodes;
CREATE TABLE IF NOT EXISTS questions_bkp AS SELECT * FROM questions;
CREATE TABLE IF NOT EXISTS user_progress_bkp AS SELECT * FROM user_progress;
CREATE TABLE IF NOT EXISTS starred_items_bkp AS SELECT * FROM starred_items;
CREATE TABLE IF NOT EXISTS learning_content_bkp AS SELECT * FROM learning_content;

-- Backup skill_learning_content if it exists
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables 
             WHERE table_name = 'skill_learning_content') THEN
    EXECUTE 'CREATE TABLE IF NOT EXISTS skill_learning_content_bkp AS SELECT * FROM skill_learning_content';
  END IF;
END $$;

-- Step 2: Drop ALL views that depend on skill_tree_nodes
DROP VIEW IF EXISTS skill_nodes_with_content_and_questions CASCADE;
DROP VIEW IF EXISTS skill_tree_hierarchy CASCADE;
DROP VIEW IF EXISTS user_skill_progress CASCADE;
DROP VIEW IF EXISTS category_stats CASCADE;

-- Step 3: Drop ALL foreign key constraints that reference skill_tree_nodes
-- Drop constraints FROM skill_tree_nodes
ALTER TABLE skill_tree_nodes DROP CONSTRAINT IF EXISTS skill_tree_nodes_parent_id_fkey;

-- Drop constraints FROM other tables TO skill_tree_nodes
ALTER TABLE questions DROP CONSTRAINT IF EXISTS questions_skill_id_fkey;
ALTER TABLE user_progress DROP CONSTRAINT IF EXISTS user_progress_skill_id_fkey;
ALTER TABLE learning_content DROP CONSTRAINT IF EXISTS learning_content_skill_id_fkey;
ALTER TABLE learning_content DROP CONSTRAINT IF EXISTS learning_content_node_id_fkey;
ALTER TABLE starred_items DROP CONSTRAINT IF EXISTS starred_items_skill_node_fkey;

-- Drop constraint from skill_learning_content
ALTER TABLE skill_learning_content DROP CONSTRAINT IF EXISTS skill_learning_content_skill_tree_node_id_fkey;

-- Drop any other potential constraints
DO $$
DECLARE
    r RECORD;
BEGIN
    -- Find and drop all foreign key constraints referencing skill_tree_nodes
    FOR r IN (
        SELECT 
            conname,
            conrelid::regclass AS table_name
        FROM pg_constraint
        WHERE contype = 'f'
        AND confrelid = 'skill_tree_nodes'::regclass
    )
    LOOP
        EXECUTE format('ALTER TABLE %s DROP CONSTRAINT IF EXISTS %I', r.table_name, r.conname);
        RAISE NOTICE 'Dropped constraint % from table %', r.conname, r.table_name;
    END LOOP;
END $$;

-- Step 4: Change column types from TEXT to UUID
-- Change skill_tree_nodes columns
ALTER TABLE skill_tree_nodes 
  ALTER COLUMN id TYPE UUID USING id::UUID,
  ALTER COLUMN parent_id TYPE UUID USING parent_id::UUID;

-- Change questions.skill_id
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='questions' AND column_name='skill_id') THEN
    ALTER TABLE questions 
      ALTER COLUMN skill_id TYPE UUID USING skill_id::UUID;
  END IF;
END $$;

-- Change user_progress.skill_id
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='user_progress' AND column_name='skill_id') THEN
    ALTER TABLE user_progress 
      ALTER COLUMN skill_id TYPE UUID USING skill_id::UUID;
  END IF;
END $$;

-- Change starred_items.item_id (only for valid UUIDs)
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
      ALTER TABLE starred_items 
        ALTER COLUMN item_id TYPE UUID USING item_id::UUID;
    ELSE
      RAISE NOTICE 'Some item_ids in starred_items are not valid UUIDs, skipping conversion';
    END IF;
  END IF;
END $$;

-- Change learning_content columns
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

-- Change skill_learning_content.skill_tree_node_id
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='skill_learning_content' AND column_name='skill_tree_node_id') THEN
    ALTER TABLE skill_learning_content 
      ALTER COLUMN skill_tree_node_id TYPE UUID USING skill_tree_node_id::UUID;
  END IF;
END $$;

-- Handle any other tables with skill/node references
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT DISTINCT
            table_name,
            column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND column_name IN ('skill_id', 'node_id', 'skill_node_id', 'skill_tree_node_id', 'category_id')
        AND table_name NOT IN ('skill_tree_nodes', 'questions', 'user_progress', 'starred_items', 'learning_content', 'skill_learning_content')
        AND data_type = 'text'
    )
    LOOP
        -- Check if the column contains valid UUIDs
        EXECUTE format('
            DO $inner$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM %I 
                    WHERE %I IS NOT NULL 
                    AND %I !~ ''^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$''
                ) THEN
                    ALTER TABLE %I ALTER COLUMN %I TYPE UUID USING %I::UUID;
                    RAISE NOTICE ''Converted %I.%I to UUID'';
                END IF;
            END $inner$;
        ', r.table_name, r.column_name, r.column_name, r.table_name, r.column_name, r.column_name, r.table_name, r.column_name);
    END LOOP;
END $$;

-- Step 5: Re-add all foreign key constraints with UUID types
-- Add constraint for skill_tree_nodes.parent_id
ALTER TABLE skill_tree_nodes 
  ADD CONSTRAINT skill_tree_nodes_parent_id_fkey 
  FOREIGN KEY (parent_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;

-- Add constraint for questions.skill_id
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='questions' AND column_name='skill_id') THEN
    ALTER TABLE questions 
      ADD CONSTRAINT questions_skill_id_fkey 
      FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
  END IF;
END $$;

-- Add constraint for user_progress.skill_id
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='user_progress' AND column_name='skill_id') THEN
    ALTER TABLE user_progress 
      ADD CONSTRAINT user_progress_skill_id_fkey 
      FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
  END IF;
END $$;

-- Add constraints for learning_content
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

-- Add constraint for skill_learning_content
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='skill_learning_content' AND column_name='skill_tree_node_id') THEN
    ALTER TABLE skill_learning_content 
      ADD CONSTRAINT skill_learning_content_skill_tree_node_id_fkey 
      FOREIGN KEY (skill_tree_node_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
  END IF;
END $$;

-- Step 6: Recreate views with only the columns that actually exist
DO $$
DECLARE
    view_query TEXT;
    select_columns TEXT := '';
    group_columns TEXT := '';
    lc_join TEXT := '';
    q_join TEXT := '';
    questions_join_column TEXT;
BEGIN
    -- Build the column list dynamically based on what exists in skill_tree_nodes
    WITH existing_columns AS (
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'skill_tree_nodes' 
        AND table_schema = 'public'
    )
    SELECT 
        string_agg('stn.' || column_name, ', ' ORDER BY 
            CASE column_name 
                WHEN 'id' THEN 1
                WHEN 'parent_id' THEN 2
                WHEN 'name' THEN 3
                WHEN 'description' THEN 4
                ELSE 99 
            END
        ) INTO select_columns
    FROM existing_columns;
    
    -- Use the same for GROUP BY
    group_columns := select_columns;
    
    -- Check what join column exists in questions table
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'questions' AND column_name = 'skill_id') THEN
        questions_join_column := 'skill_id';
    ELSIF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'questions' AND column_name = 'skill_tree_node_id') THEN
        questions_join_column := 'skill_tree_node_id';
    ELSIF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'questions' AND column_name = 'node_id') THEN
        questions_join_column := 'node_id';
    ELSIF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'questions' AND column_name = 'category_id') THEN
        questions_join_column := 'category_id';
    ELSE
        questions_join_column := NULL;
    END IF;
    
    -- Build learning_content join
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'learning_content' AND column_name = 'skill_id') THEN
        lc_join := 'LEFT JOIN learning_content lc ON lc.skill_id = stn.id';
    ELSIF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'learning_content' AND column_name = 'node_id') THEN
        lc_join := 'LEFT JOIN learning_content lc ON lc.node_id = stn.id';
    END IF;
    
    -- Build questions join
    IF questions_join_column IS NOT NULL THEN
        q_join := format('LEFT JOIN questions q ON q.%I = stn.id', questions_join_column);
    END IF;
    
    -- Build and execute the view query
    view_query := format('
    CREATE OR REPLACE VIEW skill_nodes_with_content_and_questions AS
    SELECT 
      %s,
      %s as content_count,
      %s as question_count
    FROM skill_tree_nodes stn
    %s
    %s
    GROUP BY %s',
    select_columns,
    CASE WHEN lc_join != '' THEN 'COUNT(DISTINCT lc.id)' ELSE '0::BIGINT' END,
    CASE WHEN q_join != '' THEN 'COUNT(DISTINCT q.id)' ELSE '0::BIGINT' END,
    lc_join,
    q_join,
    group_columns
    );
    
    EXECUTE view_query;
    
    RAISE NOTICE 'View created successfully';
END $$;

-- Grant permissions on views
GRANT SELECT ON skill_nodes_with_content_and_questions TO authenticated;
GRANT SELECT ON skill_nodes_with_content_and_questions TO anon;

-- Step 7: Create indexes for performance (only for columns that exist)
CREATE INDEX IF NOT EXISTS idx_skill_tree_nodes_parent_id ON skill_tree_nodes(parent_id);

-- Create indexes conditionally based on what columns exist
DO $$
BEGIN
    -- Index for questions table
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'questions' AND column_name = 'skill_id') THEN
        CREATE INDEX IF NOT EXISTS idx_questions_skill_id ON questions(skill_id);
    END IF;
    
    -- Index for user_progress table  
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user_progress' AND column_name = 'skill_id') THEN
        CREATE INDEX IF NOT EXISTS idx_user_progress_skill_id ON user_progress(skill_id);
    END IF;
    
    -- Index for starred_items table
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'starred_items' AND column_name = 'item_id') THEN
        CREATE INDEX IF NOT EXISTS idx_starred_items_item_id ON starred_items(item_id);
    END IF;
    
    -- Index for learning_content table
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'learning_content' AND column_name = 'skill_id') THEN
        CREATE INDEX IF NOT EXISTS idx_learning_content_skill_id ON learning_content(skill_id);
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'learning_content' AND column_name = 'node_id') THEN
        CREATE INDEX IF NOT EXISTS idx_learning_content_node_id ON learning_content(node_id);
    END IF;
    
    -- Index for skill_learning_content table
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'skill_learning_content' AND column_name = 'skill_tree_node_id') THEN
        CREATE INDEX IF NOT EXISTS idx_skill_learning_content_node_id ON skill_learning_content(skill_tree_node_id);
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Some indexes could not be created: %', SQLERRM;
END $$;

-- Step 8: Verify the migration
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
  
  RAISE NOTICE '✅ Migration completed successfully!';
  RAISE NOTICE '   - % rows migrated', nodes_count;
  RAISE NOTICE '   - ID column is now type: %', id_type;
  RAISE NOTICE '   - Views have been recreated';
  RAISE NOTICE '   - All foreign keys have been re-established';
  RAISE NOTICE '';
  RAISE NOTICE '⚠️  IMPORTANT: Keep backup tables until you verify everything works!';
  RAISE NOTICE '   Backup tables created: *_bkp';
END $$;

-- Step 9: List backup tables for reference
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
AND tablename LIKE '%_bkp'
ORDER BY tablename;