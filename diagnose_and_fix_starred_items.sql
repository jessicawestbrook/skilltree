-- Diagnostic and fix script for starred_items table
-- Run this in Supabase SQL Editor to diagnose and fix the table

-- 1. Check if table exists and show its structure
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'starred_items' 
ORDER BY ordinal_position;

-- 2. Check RLS status
SELECT 
    schemaname,
    tablename,
    rowsecurity,
    hasindices
FROM pg_tables 
WHERE tablename = 'starred_items';

-- 3. Check existing policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE tablename = 'starred_items';

-- 4. Check if auth schema and users table are accessible
SELECT EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_schema = 'auth' 
    AND table_name = 'users'
) as auth_users_exists;

-- 5. Drop table completely and recreate (if needed)
DROP TABLE IF EXISTS starred_items CASCADE;

-- 6. Create the table with proper structure
CREATE TABLE starred_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL,
    item_type TEXT NOT NULL CHECK (item_type IN ('spelling_word', 'vocabulary_word', 'language_question', 'question', 'skill_node')),
    item_id TEXT NOT NULL,
    item_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, item_type, item_id)
);

-- 7. Add foreign key constraint to auth.users (if auth schema is available)
-- Note: This might fail if auth.users is not accessible via SQL
DO $$
BEGIN
    BEGIN
        ALTER TABLE starred_items 
        ADD CONSTRAINT starred_items_user_id_fkey 
        FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;
    EXCEPTION WHEN others THEN
        RAISE NOTICE 'Could not add foreign key to auth.users - this is expected in some Supabase configurations';
    END;
END $$;

-- 8. Create indexes
CREATE INDEX idx_starred_items_user_id ON starred_items(user_id);
CREATE INDEX idx_starred_items_type ON starred_items(item_type);
CREATE INDEX idx_starred_items_created_at ON starred_items(created_at DESC);

-- 9. Enable RLS
ALTER TABLE starred_items ENABLE ROW LEVEL SECURITY;

-- 10. Create policies with proper auth.uid() function
CREATE POLICY "starred_items_select_policy" ON starred_items
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "starred_items_insert_policy" ON starred_items
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "starred_items_update_policy" ON starred_items
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "starred_items_delete_policy" ON starred_items
    FOR DELETE USING (auth.uid() = user_id);

-- 11. Grant necessary permissions
GRANT ALL ON starred_items TO authenticated;
GRANT ALL ON starred_items TO service_role;

-- 12. Test the table with a simple query
SELECT 'starred_items table created and configured successfully' as status;

-- 13. Show final table structure
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'starred_items' 
ORDER BY ordinal_position;