-- Migration script to ensure skill_id columns are UUID type
-- and properly reference skill_tree_nodes(id)

-- First, check current state
DO $$
BEGIN
    RAISE NOTICE 'Starting skill_id to UUID migration...';
END $$;

-- 1. Check and fix user_progress table
DO $$
BEGIN
    -- Check if skill_id column exists and its type
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'user_progress' 
        AND column_name = 'skill_id'
        AND table_schema = 'public'
    ) THEN
        -- Get the current data type
        IF EXISTS (
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name = 'user_progress' 
            AND column_name = 'skill_id'
            AND data_type != 'uuid'
            AND table_schema = 'public'
        ) THEN
            RAISE NOTICE 'Converting user_progress.skill_id to UUID...';
            
            -- Create backup first
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_progress_bkp_uuid' AND table_schema = 'public') THEN
                CREATE TABLE user_progress_bkp_uuid AS SELECT * FROM user_progress;
                RAISE NOTICE 'Created backup table user_progress_bkp_uuid';
            END IF;
            
            -- Drop existing foreign key if exists
            ALTER TABLE user_progress DROP CONSTRAINT IF EXISTS user_progress_skill_id_fkey;
            
            -- Convert column to UUID
            ALTER TABLE user_progress 
            ALTER COLUMN skill_id TYPE UUID USING skill_id::UUID;
            
            -- Add foreign key constraint
            ALTER TABLE user_progress
            ADD CONSTRAINT user_progress_skill_id_fkey 
            FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
            
            RAISE NOTICE 'Successfully converted user_progress.skill_id to UUID';
        ELSE
            RAISE NOTICE 'user_progress.skill_id is already UUID type';
        END IF;
    ELSE
        RAISE NOTICE 'user_progress.skill_id column does not exist';
    END IF;
END $$;

-- 2. Check and fix starred_categories table
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'starred_categories' 
        AND column_name = 'skill_id'
        AND table_schema = 'public'
    ) THEN
        IF EXISTS (
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name = 'starred_categories' 
            AND column_name = 'skill_id'
            AND data_type != 'uuid'
            AND table_schema = 'public'
        ) THEN
            RAISE NOTICE 'Converting starred_categories.skill_id to UUID...';
            
            -- Create backup first
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'starred_categories_bkp_uuid' AND table_schema = 'public') THEN
                CREATE TABLE starred_categories_bkp_uuid AS SELECT * FROM starred_categories;
                RAISE NOTICE 'Created backup table starred_categories_bkp_uuid';
            END IF;
            
            -- Drop existing foreign key if exists
            ALTER TABLE starred_categories DROP CONSTRAINT IF EXISTS starred_categories_skill_id_fkey;
            
            -- Convert column to UUID
            ALTER TABLE starred_categories 
            ALTER COLUMN skill_id TYPE UUID USING skill_id::UUID;
            
            -- Add foreign key constraint
            ALTER TABLE starred_categories
            ADD CONSTRAINT starred_categories_skill_id_fkey 
            FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
            
            RAISE NOTICE 'Successfully converted starred_categories.skill_id to UUID';
        ELSE
            RAISE NOTICE 'starred_categories.skill_id is already UUID type';
        END IF;
    ELSE
        RAISE NOTICE 'starred_categories.skill_id column does not exist';
    END IF;
END $$;

-- 3. Check and fix starred_items table (if it has skill_id)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'starred_items' 
        AND column_name = 'skill_id'
        AND table_schema = 'public'
    ) THEN
        IF EXISTS (
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name = 'starred_items' 
            AND column_name = 'skill_id'
            AND data_type != 'uuid'
            AND table_schema = 'public'
        ) THEN
            RAISE NOTICE 'Converting starred_items.skill_id to UUID...';
            
            -- Create backup first
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'starred_items_bkp_uuid' AND table_schema = 'public') THEN
                CREATE TABLE starred_items_bkp_uuid AS SELECT * FROM starred_items;
                RAISE NOTICE 'Created backup table starred_items_bkp_uuid';
            END IF;
            
            -- Drop existing foreign key if exists
            ALTER TABLE starred_items DROP CONSTRAINT IF EXISTS starred_items_skill_id_fkey;
            
            -- Convert column to UUID
            ALTER TABLE starred_items 
            ALTER COLUMN skill_id TYPE UUID USING skill_id::UUID;
            
            -- Add foreign key constraint
            ALTER TABLE starred_items
            ADD CONSTRAINT starred_items_skill_id_fkey 
            FOREIGN KEY (skill_id) REFERENCES skill_tree_nodes(id) ON DELETE CASCADE;
            
            RAISE NOTICE 'Successfully converted starred_items.skill_id to UUID';
        ELSE
            RAISE NOTICE 'starred_items.skill_id is already UUID type';
        END IF;
    ELSE
        RAISE NOTICE 'starred_items.skill_id column does not exist';
    END IF;
END $$;

-- 4. Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_progress_skill_id ON user_progress(skill_id);
CREATE INDEX IF NOT EXISTS idx_starred_categories_skill_id ON starred_categories(skill_id);
CREATE INDEX IF NOT EXISTS idx_starred_items_skill_id ON starred_items(skill_id) WHERE skill_id IS NOT NULL;

-- 5. Verify the changes
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
    AND column_name = 'skill_id'
ORDER BY table_name;

-- Show foreign key constraints
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND kcu.column_name = 'skill_id'
    AND tc.table_schema = 'public';

RAISE NOTICE 'Migration completed successfully!';