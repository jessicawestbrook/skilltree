-- Migration script to rename node_id and skill_node_id to skill_id across the database
-- This script creates backups first, then renames columns

-- ============================================
-- STEP 1: CREATE BACKUP TABLES
-- ============================================

-- Check if backup tables exist and increment if needed
DO $$
DECLARE
    backup_suffix TEXT := '_bkp';
    counter INT := 1;
BEGIN
    -- Find the next available backup suffix for user_progress
    WHILE EXISTS (SELECT 1 FROM information_schema.tables 
                  WHERE table_schema = 'public' 
                  AND table_name = 'user_progress' || backup_suffix) LOOP
        counter := counter + 1;
        backup_suffix := '_bkp' || counter;
    END LOOP;
    
    -- Create backup of user_progress
    EXECUTE format('CREATE TABLE public.user_progress%s AS SELECT * FROM public.user_progress', backup_suffix);
    RAISE NOTICE 'Created backup table: user_progress%', backup_suffix;
END $$;

DO $$
DECLARE
    backup_suffix TEXT := '_bkp';
    counter INT := 1;
BEGIN
    -- Find the next available backup suffix for starred_categories
    WHILE EXISTS (SELECT 1 FROM information_schema.tables 
                  WHERE table_schema = 'public' 
                  AND table_name = 'starred_categories' || backup_suffix) LOOP
        counter := counter + 1;
        backup_suffix := '_bkp' || counter;
    END LOOP;
    
    -- Create backup of starred_categories if it exists
    IF EXISTS (SELECT 1 FROM information_schema.tables 
               WHERE table_schema = 'public' 
               AND table_name = 'starred_categories') THEN
        EXECUTE format('CREATE TABLE public.starred_categories%s AS SELECT * FROM public.starred_categories', backup_suffix);
        RAISE NOTICE 'Created backup table: starred_categories%', backup_suffix;
    END IF;
END $$;

-- ============================================
-- STEP 2: RENAME COLUMNS IN TABLES
-- ============================================

-- Rename skill_node_id to skill_id in user_progress table
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_schema = 'public' 
               AND table_name = 'user_progress' 
               AND column_name = 'skill_node_id') THEN
        
        -- Drop existing foreign key constraints
        ALTER TABLE public.user_progress 
        DROP CONSTRAINT IF EXISTS user_progress_skill_node_id_fkey;
        
        -- Rename the column
        ALTER TABLE public.user_progress 
        RENAME COLUMN skill_node_id TO skill_id;
        
        -- Re-add foreign key constraint with new name
        ALTER TABLE public.user_progress 
        ADD CONSTRAINT user_progress_skill_id_fkey 
        FOREIGN KEY (skill_id) 
        REFERENCES public.skill_tree_nodes(id) 
        ON DELETE CASCADE;
        
        RAISE NOTICE 'Renamed user_progress.skill_node_id to skill_id';
    END IF;
END $$;

-- Rename skill_node_id to skill_id in starred_categories table
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_schema = 'public' 
               AND table_name = 'starred_categories' 
               AND column_name = 'skill_node_id') THEN
        
        -- Drop existing foreign key constraints
        ALTER TABLE public.starred_categories 
        DROP CONSTRAINT IF EXISTS starred_categories_skill_node_id_fkey;
        
        -- Rename the column
        ALTER TABLE public.starred_categories 
        RENAME COLUMN skill_node_id TO skill_id;
        
        -- Re-add foreign key constraint with new name
        ALTER TABLE public.starred_categories 
        ADD CONSTRAINT starred_categories_skill_id_fkey 
        FOREIGN KEY (skill_id) 
        REFERENCES public.skill_tree_nodes(id) 
        ON DELETE CASCADE;
        
        RAISE NOTICE 'Renamed starred_categories.skill_node_id to skill_id';
    END IF;
END $$;

-- Check and rename node_id to skill_id in questions table if it exists
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_schema = 'public' 
               AND table_name = 'questions' 
               AND column_name = 'node_id') THEN
        
        -- Drop existing foreign key constraints if any
        ALTER TABLE public.questions 
        DROP CONSTRAINT IF EXISTS questions_node_id_fkey;
        
        -- Rename the column
        ALTER TABLE public.questions 
        RENAME COLUMN node_id TO skill_id;
        
        -- Add foreign key constraint if the column should reference skill_tree_nodes
        -- ALTER TABLE public.questions 
        -- ADD CONSTRAINT questions_skill_id_fkey 
        -- FOREIGN KEY (skill_id) 
        -- REFERENCES public.skill_tree_nodes(id) 
        -- ON DELETE CASCADE;
        
        RAISE NOTICE 'Renamed questions.node_id to skill_id';
    END IF;
END $$;

-- Check for money_counting_progress table and rename skill_tree_node_id if it exists
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_schema = 'public' 
               AND table_name = 'money_counting_progress' 
               AND column_name = 'skill_tree_node_id') THEN
        
        -- Drop existing foreign key constraints
        ALTER TABLE public.money_counting_progress 
        DROP CONSTRAINT IF EXISTS money_counting_progress_skill_tree_node_id_fkey;
        
        -- Rename the column
        ALTER TABLE public.money_counting_progress 
        RENAME COLUMN skill_tree_node_id TO skill_id;
        
        -- Re-add foreign key constraint with new name
        ALTER TABLE public.money_counting_progress 
        ADD CONSTRAINT money_counting_progress_skill_id_fkey 
        FOREIGN KEY (skill_id) 
        REFERENCES public.skill_tree_nodes(id) 
        ON DELETE CASCADE;
        
        RAISE NOTICE 'Renamed money_counting_progress.skill_tree_node_id to skill_id';
    END IF;
END $$;

-- ============================================
-- STEP 3: UPDATE RLS POLICIES
-- ============================================

-- Update RLS policies for user_progress if they reference skill_node_id
DO $$
BEGIN
    -- Drop and recreate policies with updated column names
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

-- Update RLS policies for starred_categories if it exists
DO $$
BEGIN
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
-- STEP 4: VERIFY CHANGES
-- ============================================

-- Display the updated column names
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
    AND table_name IN ('user_progress', 'starred_categories', 'questions', 'money_counting_progress')
    AND column_name IN ('skill_id', 'skill_node_id', 'node_id', 'skill_tree_node_id')
ORDER BY table_name, column_name;