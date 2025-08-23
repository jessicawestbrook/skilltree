-- Safe migration script that handles type mismatches
-- This properly handles integer vs text column types

-- ============================================
-- STEP 1: CHECK CURRENT STATE
-- ============================================

DO $$
BEGIN
    RAISE NOTICE 'Starting safe migration to standardize skill_id columns...';
    RAISE NOTICE '';
END $$;

-- ============================================
-- STEP 2: HANDLE USER_PROGRESS TABLE
-- ============================================

DO $$
DECLARE
    has_skill_id BOOLEAN;
    has_skill_node_id BOOLEAN;
    skill_id_type TEXT;
    skill_node_id_type TEXT;
    target_type TEXT;
BEGIN
    -- Check what columns exist
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'user_progress' 
        AND column_name = 'skill_id'
    ) INTO has_skill_id;
    
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'user_progress' 
        AND column_name = 'skill_node_id'
    ) INTO has_skill_node_id;
    
    -- Get the data type of skill_tree_nodes.id (the target type)
    SELECT data_type INTO target_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
        AND table_name = 'skill_tree_nodes'
        AND column_name = 'id';
    
    RAISE NOTICE 'Target type from skill_tree_nodes.id: %', target_type;
    
    IF has_skill_id AND has_skill_node_id THEN
        -- Both columns exist
        RAISE NOTICE 'user_progress: Both skill_id and skill_node_id exist.';
        
        -- Get the data types
        SELECT data_type INTO skill_id_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
            AND table_name = 'user_progress'
            AND column_name = 'skill_id';
            
        SELECT data_type INTO skill_node_id_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
            AND table_name = 'user_progress'
            AND column_name = 'skill_node_id';
            
        RAISE NOTICE 'skill_id type: %, skill_node_id type: %', skill_id_type, skill_node_id_type;
        
        -- Determine which column to keep based on type matching
        IF skill_id_type = target_type THEN
            -- skill_id has the correct type, drop skill_node_id
            RAISE NOTICE 'Keeping skill_id (correct type), dropping skill_node_id';
            ALTER TABLE public.user_progress DROP COLUMN IF EXISTS skill_node_id;
        ELSIF skill_node_id_type = target_type THEN
            -- skill_node_id has the correct type, need to fix skill_id
            RAISE NOTICE 'skill_node_id has correct type, fixing skill_id';
            
            -- Drop the incorrect skill_id column
            ALTER TABLE public.user_progress DROP COLUMN IF EXISTS skill_id;
            
            -- Rename skill_node_id to skill_id
            ALTER TABLE public.user_progress RENAME COLUMN skill_node_id TO skill_id;
        ELSE
            -- Neither matches, create new column with correct type
            RAISE NOTICE 'Neither column has correct type, creating new skill_id';
            
            -- Drop both old columns
            ALTER TABLE public.user_progress DROP COLUMN IF EXISTS skill_id;
            ALTER TABLE public.user_progress DROP COLUMN IF EXISTS skill_node_id;
            
            -- Add new column with correct type
            IF target_type = 'text' OR target_type = 'character varying' THEN
                ALTER TABLE public.user_progress ADD COLUMN skill_id TEXT;
            ELSIF target_type = 'uuid' THEN
                ALTER TABLE public.user_progress ADD COLUMN skill_id UUID;
            ELSIF target_type = 'integer' THEN
                ALTER TABLE public.user_progress ADD COLUMN skill_id INTEGER;
            ELSIF target_type = 'bigint' THEN
                ALTER TABLE public.user_progress ADD COLUMN skill_id BIGINT;
            ELSE
                RAISE EXCEPTION 'Unsupported target type: %', target_type;
            END IF;
        END IF;
        
    ELSIF has_skill_node_id AND NOT has_skill_id THEN
        -- Only skill_node_id exists - check its type
        SELECT data_type INTO skill_node_id_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
            AND table_name = 'user_progress'
            AND column_name = 'skill_node_id';
            
        IF skill_node_id_type = target_type THEN
            -- Type is correct, just rename
            RAISE NOTICE 'user_progress: Renaming skill_node_id to skill_id';
            ALTER TABLE public.user_progress RENAME COLUMN skill_node_id TO skill_id;
        ELSE
            -- Type is wrong, need to recreate
            RAISE NOTICE 'user_progress: skill_node_id has wrong type, recreating as skill_id';
            
            -- Save the data first if there is any
            CREATE TEMP TABLE temp_user_progress_data AS
            SELECT user_id, skill_node_id::text as skill_ref, status, rating, last_accessed
            FROM public.user_progress
            WHERE skill_node_id IS NOT NULL;
            
            -- Drop old column
            ALTER TABLE public.user_progress DROP COLUMN skill_node_id;
            
            -- Add new column with correct type
            IF target_type = 'text' OR target_type = 'character varying' THEN
                ALTER TABLE public.user_progress ADD COLUMN skill_id TEXT;
            ELSIF target_type = 'uuid' THEN
                ALTER TABLE public.user_progress ADD COLUMN skill_id UUID;
            ELSIF target_type = 'integer' THEN
                ALTER TABLE public.user_progress ADD COLUMN skill_id INTEGER;
            ELSIF target_type = 'bigint' THEN
                ALTER TABLE public.user_progress ADD COLUMN skill_id BIGINT;
            END IF;
            
            -- Restore data if temp table was created
            IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'temp_user_progress_data') THEN
                IF target_type IN ('text', 'character varying') THEN
                    UPDATE public.user_progress p
                    SET skill_id = t.skill_ref
                    FROM temp_user_progress_data t
                    WHERE p.user_id = t.user_id;
                END IF;
                DROP TABLE IF EXISTS temp_user_progress_data;
            END IF;
        END IF;
        
    ELSIF has_skill_id AND NOT has_skill_node_id THEN
        -- Already migrated, check type
        SELECT data_type INTO skill_id_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
            AND table_name = 'user_progress'
            AND column_name = 'skill_id';
            
        IF skill_id_type = target_type THEN
            RAISE NOTICE 'user_progress: Already has skill_id with correct type';
        ELSE
            RAISE NOTICE 'user_progress: skill_id exists but has wrong type (%), should be %', skill_id_type, target_type;
            -- For safety, don't automatically change existing data
            RAISE WARNING 'Manual intervention may be needed to fix type mismatch';
        END IF;
        
    ELSE
        RAISE NOTICE 'user_progress: No skill-related columns found';
    END IF;
    
    -- Ensure foreign key constraint exists with correct name
    ALTER TABLE public.user_progress 
    DROP CONSTRAINT IF EXISTS user_progress_skill_node_id_fkey;
    
    ALTER TABLE public.user_progress 
    DROP CONSTRAINT IF EXISTS user_progress_skill_id_fkey;
    
    IF has_skill_id OR has_skill_node_id THEN
        -- Only add constraint if column exists and has correct type
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_schema = 'public' 
                   AND table_name = 'user_progress' 
                   AND column_name = 'skill_id') THEN
            ALTER TABLE public.user_progress 
            ADD CONSTRAINT user_progress_skill_id_fkey 
            FOREIGN KEY (skill_id) 
            REFERENCES public.skill_tree_nodes(id) 
            ON DELETE CASCADE;
            RAISE NOTICE 'user_progress: Added foreign key constraint';
        END IF;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in user_progress migration: %', SQLERRM;
        RAISE;
END $$;

-- ============================================
-- STEP 3: UPDATE RLS POLICIES
-- ============================================

DO $$
BEGIN
    -- Update RLS policies for user_progress
    DROP POLICY IF EXISTS "Users can view own progress" ON public.user_progress;
    DROP POLICY IF EXISTS "Users can manage own progress" ON public.user_progress;
    
    CREATE POLICY "Users can view own progress" 
    ON public.user_progress 
    FOR SELECT 
    USING (auth.uid() = user_id);
    
    CREATE POLICY "Users can manage own progress" 
    ON public.user_progress 
    FOR ALL 
    USING (auth.uid() = user_id);
    
    RAISE NOTICE 'Updated RLS policies for user_progress';
END $$;

-- ============================================
-- STEP 4: FINAL VERIFICATION
-- ============================================

DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '=== Migration Complete ===';
    RAISE NOTICE 'Please review the column structure below:';
END $$;

-- Show final state of columns
SELECT 
    table_name,
    column_name,
    data_type,
    udt_name
FROM information_schema.columns
WHERE table_schema = 'public'
    AND table_name = 'user_progress'
    AND column_name IN ('skill_id', 'skill_node_id', 'user_id')
ORDER BY column_name;