-- Test RLS policies for starred_items table
-- Run this in Supabase SQL Editor while logged in as a user

-- 1. Check current user
SELECT auth.uid() as current_user_id;

-- 2. Check if RLS is enabled
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables 
WHERE tablename = 'starred_items';

-- 3. Check existing policies
SELECT 
    policyname,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE tablename = 'starred_items';

-- 4. Test basic select (should work with RLS)
SELECT COUNT(*) as total_starred_items FROM starred_items;

-- 5. Test insert (this should work if user is authenticated)
INSERT INTO starred_items (user_id, item_type, item_id, item_data)
VALUES (auth.uid(), 'skill_node', 'test-category-id', '{"test": true}')
ON CONFLICT (user_id, item_type, item_id) DO NOTHING;

-- 6. Test select with user filter (this is what the app is trying to do)
SELECT * FROM starred_items 
WHERE user_id = auth.uid() 
AND item_type = 'skill_node' 
AND item_id = 'test-category-id';

-- 7. Clean up test data
DELETE FROM starred_items 
WHERE user_id = auth.uid() 
AND item_type = 'skill_node' 
AND item_id = 'test-category-id';

-- 8. Check table structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'starred_items' 
ORDER BY ordinal_position;