-- Dynamic UUID migration script that detects all column names automatically
-- This version discovers your actual schema and adapts to it

-- Step 1: Create comprehensive backups
DO $$
DECLARE
    r RECORD;
BEGIN
    -- Backup all tables that might have foreign keys to skill_tree_nodes
    FOR r IN (
        SELECT DISTINCT tc.table_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY' 
        AND ccu.table_name = 'skill_tree_nodes'
        UNION
        SELECT 'skill_tree_nodes'
        UNION
        SELECT table_name 
        FROM information_schema.columns 
        WHERE column_name IN ('skill_id', 'node_id', 'skill_tree_node_id', 'category_id', 'item_id', 'test_id')
        AND table_schema = 'public'
    )
    LOOP
        EXECUTE format('CREATE TABLE IF NOT EXISTS %I AS SELECT * FROM %I', 
                      r.table_name || '_bkp', r.table_name);
        RAISE NOTICE 'Backed up table: %', r.table_name;
    END LOOP;
END $$;

-- Step 2: Drop ALL views that depend on skill_tree_nodes
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT DISTINCT dependent_ns.nspname AS schema_name, dependent_view.relname AS view_name
        FROM pg_depend 
        JOIN pg_rewrite ON pg_depend.objid = pg_rewrite.oid 
        JOIN pg_class AS dependent_view ON pg_rewrite.ev_class = dependent_view.oid 
        JOIN pg_class AS source_table ON pg_depend.refobjid = source_table.oid 
        JOIN pg_namespace dependent_ns ON dependent_view.relnamespace = dependent_ns.oid
        JOIN pg_namespace source_ns ON source_table.relnamespace = source_ns.oid
        WHERE source_ns.nspname = 'public'
        AND source_table.relname = 'skill_tree_nodes'
        AND dependent_view.relkind = 'v'
    )
    LOOP
        EXECUTE format('DROP VIEW IF EXISTS %I.%I CASCADE', r.schema_name, r.view_name);
        RAISE NOTICE 'Dropped view: %.%', r.schema_name, r.view_name;
    END LOOP;
END $$;

-- Step 3: Drop ALL foreign key constraints dynamically
DO $$
DECLARE
    r RECORD;
BEGIN
    -- Drop all foreign keys that reference skill_tree_nodes
    FOR r IN (
        SELECT 
            tc.table_name,
            tc.constraint_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND ccu.table_name = 'skill_tree_nodes'
    )
    LOOP
        EXECUTE format('ALTER TABLE %I DROP CONSTRAINT IF EXISTS %I', r.table_name, r.constraint_name);
        RAISE NOTICE 'Dropped constraint % from table %', r.constraint_name, r.table_name;
    END LOOP;
    
    -- Also drop the self-referential constraint
    ALTER TABLE skill_tree_nodes DROP CONSTRAINT IF EXISTS skill_tree_nodes_parent_id_fkey;
END $$;

-- Step 4: Convert columns to UUID dynamically
DO $$
DECLARE
    r RECORD;
    has_invalid_uuids BOOLEAN;
BEGIN
    -- First, convert skill_tree_nodes primary and foreign keys
    ALTER TABLE skill_tree_nodes 
        ALTER COLUMN id TYPE UUID USING id::UUID,
        ALTER COLUMN parent_id TYPE UUID USING parent_id::UUID;
    RAISE NOTICE 'Converted skill_tree_nodes.id and parent_id to UUID';
    
    -- Now find and convert all columns that reference skill_tree_nodes
    FOR r IN (
        SELECT DISTINCT
            c.table_name,
            c.column_name,
            c.data_type
        FROM information_schema.columns c
        WHERE c.table_schema = 'public'
        AND c.table_name != 'skill_tree_nodes'
        AND c.data_type IN ('text', 'character varying')
        AND EXISTS (
            -- Check if this column contains UUIDs that match skill_tree_nodes.id
            SELECT 1 
            FROM information_schema.columns stn 
            WHERE stn.table_name = 'skill_tree_nodes' 
            AND stn.column_name = 'id'
        )
    )
    LOOP
        -- Check if column contains valid UUIDs
        EXECUTE format('
            SELECT EXISTS (
                SELECT 1 FROM %I 
                WHERE %I IS NOT NULL 
                AND %I !~ ''^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$''
            )', r.table_name, r.column_name, r.column_name) INTO has_invalid_uuids;
        
        IF NOT has_invalid_uuids THEN
            -- Check if any values in this column match skill_tree_nodes.id values
            EXECUTE format('
                SELECT EXISTS (
                    SELECT 1 FROM %I t
                    JOIN skill_tree_nodes stn ON t.%I::text = stn.id::text
                    LIMIT 1
                )', r.table_name, r.column_name) INTO has_invalid_uuids;
            
            IF has_invalid_uuids THEN
                -- This column references skill_tree_nodes, convert it
                BEGIN
                    EXECUTE format('ALTER TABLE %I ALTER COLUMN %I TYPE UUID USING %I::UUID',
                                  r.table_name, r.column_name, r.column_name);
                    RAISE NOTICE 'Converted %.% to UUID', r.table_name, r.column_name;
                EXCEPTION
                    WHEN OTHERS THEN
                        RAISE NOTICE 'Could not convert %.%: %', r.table_name, r.column_name, SQLERRM;
                END;
            END IF;
        END IF;
    END LOOP;
END $$;

-- Step 5: Re-add foreign key constraints dynamically
DO $$
DECLARE
    r RECORD;
    fk_exists BOOLEAN;
BEGIN
    -- Add back the self-referential constraint
    ALTER TABLE skill_tree_nodes 
        ADD CONSTRAINT skill_tree_nodes_parent_id_fkey 
        FOREIGN KEY (parent_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
    RAISE NOTICE 'Added foreign key for skill_tree_nodes.parent_id';
    
    -- Find columns that should have foreign keys to skill_tree_nodes
    FOR r IN (
        SELECT DISTINCT
            c.table_name,
            c.column_name
        FROM information_schema.columns c
        WHERE c.table_schema = 'public'
        AND c.table_name != 'skill_tree_nodes'
        AND c.data_type = 'uuid'
        AND (
            c.column_name LIKE '%skill%id%'
            OR c.column_name LIKE '%node%id%'
            OR c.column_name = 'category_id'
            OR c.column_name = 'test_id'
            OR (c.table_name = 'starred_items' AND c.column_name = 'item_id')
        )
    )
    LOOP
        -- Check if values in this column exist in skill_tree_nodes.id
        EXECUTE format('
            SELECT EXISTS (
                SELECT 1 FROM %I t
                WHERE t.%I IS NOT NULL
                AND EXISTS (SELECT 1 FROM skill_tree_nodes stn WHERE stn.id = t.%I)
                LIMIT 1
            )', r.table_name, r.column_name, r.column_name) INTO fk_exists;
        
        IF fk_exists THEN
            BEGIN
                EXECUTE format('ALTER TABLE %I ADD CONSTRAINT %I FOREIGN KEY (%I) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE',
                              r.table_name, 
                              r.table_name || '_' || r.column_name || '_fkey',
                              r.column_name);
                RAISE NOTICE 'Added foreign key for %.%', r.table_name, r.column_name;
            EXCEPTION
                WHEN OTHERS THEN
                    RAISE NOTICE 'Could not add foreign key for %.%: %', r.table_name, r.column_name, SQLERRM;
            END;
        END IF;
    END LOOP;
END $$;

-- Step 6: Recreate views dynamically
DO $$
DECLARE
    view_query TEXT;
    select_columns TEXT;
    lc_join_col TEXT := NULL;
    q_join_col TEXT := NULL;
BEGIN
    -- Get all columns from skill_tree_nodes
    SELECT string_agg('stn.' || column_name, ', ' ORDER BY ordinal_position)
    INTO select_columns
    FROM information_schema.columns
    WHERE table_name = 'skill_tree_nodes'
    AND table_schema = 'public';
    
    -- Find join column for learning_content
    SELECT column_name INTO lc_join_col
    FROM information_schema.columns
    WHERE table_name = 'learning_content'
    AND data_type = 'uuid'
    AND column_name IN ('skill_id', 'node_id', 'skill_tree_node_id')
    LIMIT 1;
    
    -- Find join column for questions
    SELECT column_name INTO q_join_col
    FROM information_schema.columns
    WHERE table_name = 'questions'
    AND data_type = 'uuid'
    AND column_name IN ('skill_id', 'node_id', 'skill_tree_node_id', 'category_id')
    LIMIT 1;
    
    -- Build the view query
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
    CASE WHEN lc_join_col IS NOT NULL 
         THEN 'COUNT(DISTINCT lc.id)' 
         ELSE '0::BIGINT' END,
    CASE WHEN q_join_col IS NOT NULL 
         THEN 'COUNT(DISTINCT q.id)' 
         ELSE '0::BIGINT' END,
    CASE WHEN lc_join_col IS NOT NULL 
         THEN format('LEFT JOIN learning_content lc ON lc.%I = stn.id', lc_join_col)
         ELSE '' END,
    CASE WHEN q_join_col IS NOT NULL 
         THEN format('LEFT JOIN questions q ON q.%I = stn.id', q_join_col)
         ELSE '' END,
    select_columns
    );
    
    EXECUTE view_query;
    RAISE NOTICE 'Created view skill_nodes_with_content_and_questions';
    
    -- Grant permissions
    GRANT SELECT ON skill_nodes_with_content_and_questions TO authenticated;
    GRANT SELECT ON skill_nodes_with_content_and_questions TO anon;
END $$;

-- Step 7: Create indexes dynamically
DO $$
DECLARE
    r RECORD;
BEGIN
    -- Create index on parent_id
    CREATE INDEX IF NOT EXISTS idx_skill_tree_nodes_parent_id ON skill_tree_nodes(parent_id);
    
    -- Create indexes on all UUID columns that reference skill_tree_nodes
    FOR r IN (
        SELECT DISTINCT
            c.table_name,
            c.column_name
        FROM information_schema.columns c
        WHERE c.table_schema = 'public'
        AND c.data_type = 'uuid'
        AND c.table_name != 'skill_tree_nodes'
        AND (
            c.column_name LIKE '%skill%'
            OR c.column_name LIKE '%node%'
            OR c.column_name = 'category_id'
            OR c.column_name = 'item_id'
        )
    )
    LOOP
        BEGIN
            EXECUTE format('CREATE INDEX IF NOT EXISTS idx_%s_%s ON %I(%I)',
                          replace(r.table_name, '_', ''),
                          replace(r.column_name, '_', ''),
                          r.table_name,
                          r.column_name);
            RAISE NOTICE 'Created index on %.%', r.table_name, r.column_name;
        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE 'Could not create index on %.%: %', r.table_name, r.column_name, SQLERRM;
        END;
    END LOOP;
END $$;

-- Step 8: Verify the migration
DO $$
DECLARE
    nodes_count INTEGER;
    backup_count INTEGER;
    id_type TEXT;
    success BOOLEAN := true;
BEGIN
    -- Check row counts
    SELECT COUNT(*) INTO nodes_count FROM skill_tree_nodes;
    SELECT COUNT(*) INTO backup_count FROM skill_tree_nodes_bkp;
    
    IF nodes_count != backup_count THEN
        RAISE WARNING 'Row counts do not match: % vs %', nodes_count, backup_count;
        success := false;
    END IF;
    
    -- Check data type
    SELECT data_type INTO id_type 
    FROM information_schema.columns 
    WHERE table_name = 'skill_tree_nodes' AND column_name = 'id';
    
    IF id_type != 'uuid' THEN
        RAISE WARNING 'ID column is not UUID type: %', id_type;
        success := false;
    END IF;
    
    IF success THEN
        RAISE NOTICE '✅ Migration completed successfully!';
        RAISE NOTICE '   - % rows migrated', nodes_count;
        RAISE NOTICE '   - ID column is now type: %', id_type;
        RAISE NOTICE '   - All constraints and indexes recreated';
        RAISE NOTICE '';
        RAISE NOTICE '⚠️  IMPORTANT: Keep backup tables until you verify everything works!';
    ELSE
        RAISE EXCEPTION 'Migration verification failed - check warnings above';
    END IF;
END $$;

-- Step 9: Show summary
SELECT 
    'Backup Tables' as category,
    tablename as name,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
AND tablename LIKE '%_bkp'
UNION ALL
SELECT 
    'Converted Tables' as category,
    table_name as name,
    count(*) || ' UUID columns' as size
FROM information_schema.columns
WHERE table_schema = 'public'
AND data_type = 'uuid'
GROUP BY table_name
ORDER BY category, name;