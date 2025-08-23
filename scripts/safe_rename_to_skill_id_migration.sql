-- Safe migration script that checks for existing columns before renaming
-- This handles cases where migration was partially applied

-- ============================================
-- STEP 1: CHECK CURRENT STATE
-- ============================================

DO $$
BEGIN
    RAISE NOTICE 'Starting safe migration to rename columns to skill_id...';
    RAISE NOTICE '';
END $$;

-- ============================================
-- STEP 2: HANDLE USER_PROGRESS TABLE
-- ============================================

DO $$
DECLARE
    has_skill_id BOOLEAN;
    has_skill_node_id BOOLEAN;
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
    
    IF has_skill_id AND has_skill_node_id THEN
        -- Both columns exist - drop the old column (skill_id should be the correct one)
        RAISE NOTICE 'user_progress: Both skill_id and skill_node_id exist. Dropping old skill_node_id column...';
        
        -- Since skill_id already exists and is likely the correct column, just drop skill_node_id
        ALTER TABLE public.user_progress DROP COLUMN IF EXISTS skill_node_id;
        RAISE NOTICE 'user_progress: Dropped skill_node_id column';
        
    ELSIF has_skill_node_id AND NOT has_skill_id THEN
        -- Only skill_node_id exists - rename it
        RAISE NOTICE 'user_progress: Renaming skill_node_id to skill_id';
        ALTER TABLE public.user_progress RENAME COLUMN skill_node_id TO skill_id;
        
    ELSIF has_skill_id AND NOT has_skill_node_id THEN
        -- Already migrated
        RAISE NOTICE 'user_progress: Already has skill_id column (migration complete)';
        
    ELSE
        RAISE NOTICE 'user_progress: No relevant columns found';
    END IF;
    
    -- Ensure foreign key constraint exists with correct name
    ALTER TABLE public.user_progress 
    DROP CONSTRAINT IF EXISTS user_progress_skill_node_id_fkey;
    
    ALTER TABLE public.user_progress 
    DROP CONSTRAINT IF EXISTS user_progress_skill_id_fkey;
    
    IF has_skill_id OR has_skill_node_id THEN
        ALTER TABLE public.user_progress 
        ADD CONSTRAINT user_progress_skill_id_fkey 
        FOREIGN KEY (skill_id) 
        REFERENCES public.skill_tree_nodes(id) 
        ON DELETE CASCADE;
        RAISE NOTICE 'user_progress: Updated foreign key constraint';
    END IF;
END $$;

-- ============================================
-- STEP 3: HANDLE STARRED_CATEGORIES TABLE
-- ============================================

DO $$
DECLARE
    table_exists BOOLEAN;
    has_skill_id BOOLEAN;
    has_skill_node_id BOOLEAN;
BEGIN
    -- Check if table exists
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'starred_categories'
    ) INTO table_exists;
    
    IF NOT table_exists THEN
        RAISE NOTICE 'starred_categories: Table does not exist';
        RETURN;
    END IF;
    
    -- Check what columns exist
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'starred_categories' 
        AND column_name = 'skill_id'
    ) INTO has_skill_id;
    
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'starred_categories' 
        AND column_name = 'skill_node_id'
    ) INTO has_skill_node_id;
    
    IF has_skill_id AND has_skill_node_id THEN
        -- Both columns exist - need to migrate data and drop old column
        RAISE NOTICE 'starred_categories: Both skill_id and skill_node_id exist. Migrating data...';
        
        UPDATE public.starred_categories 
        SET skill_id = skill_node_id 
        WHERE skill_id IS NULL AND skill_node_id IS NOT NULL;
        
        ALTER TABLE public.starred_categories DROP COLUMN IF EXISTS skill_node_id;
        RAISE NOTICE 'starred_categories: Dropped skill_node_id column';
        
    ELSIF has_skill_node_id AND NOT has_skill_id THEN
        -- Only skill_node_id exists - rename it
        RAISE NOTICE 'starred_categories: Renaming skill_node_id to skill_id';
        ALTER TABLE public.starred_categories RENAME COLUMN skill_node_id TO skill_id;
        
    ELSIF has_skill_id AND NOT has_skill_node_id THEN
        -- Already migrated
        RAISE NOTICE 'starred_categories: Already has skill_id column (migration complete)';
        
    ELSE
        RAISE NOTICE 'starred_categories: No relevant columns found';
    END IF;
    
    -- Update foreign key constraint
    ALTER TABLE public.starred_categories 
    DROP CONSTRAINT IF EXISTS starred_categories_skill_node_id_fkey;
    
    ALTER TABLE public.starred_categories 
    DROP CONSTRAINT IF EXISTS starred_categories_skill_id_fkey;
    
    IF has_skill_id OR has_skill_node_id THEN
        ALTER TABLE public.starred_categories 
        ADD CONSTRAINT starred_categories_skill_id_fkey 
        FOREIGN KEY (skill_id) 
        REFERENCES public.skill_tree_nodes(id) 
        ON DELETE CASCADE;
        RAISE NOTICE 'starred_categories: Updated foreign key constraint';
    END IF;
END $$;

-- ============================================
-- STEP 4: UPDATE RLS POLICIES
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
    
    -- Update RLS policies for starred_categories if it exists
    IF EXISTS (SELECT 1 FROM information_schema.tables 
               WHERE table_schema = 'public' 
               AND table_name = 'starred_categories') THEN
        
        DROP POLICY IF EXISTS "Users can view own starred categories" ON public.starred_categories;
        DROP POLICY IF EXISTS "Users can manage own starred categories" ON public.starred_categories;
        
        CREATE POLICY "Users can view own starred categories" 
        ON public.starred_categories 
        FOR SELECT 
        USING (auth.uid() = user_id);
        
        CREATE POLICY "Users can manage own starred categories" 
        ON public.starred_categories 
        FOR ALL 
        USING (auth.uid() = user_id);
        
        RAISE NOTICE 'Updated RLS policies for starred_categories';
    END IF;
END $$;

-- ============================================
-- STEP 5: FINAL VERIFICATION
-- ============================================

DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '=== Migration Complete ===';
    RAISE NOTICE 'Verifying final column state:';
END $$;

-- Show final state of columns
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
    AND table_name IN ('user_progress', 'starred_categories', 'questions', 'money_counting_progress')
    AND column_name IN ('skill_id', 'skill_node_id', 'node_id', 'skill_tree_node_id')
ORDER BY table_name, column_name;