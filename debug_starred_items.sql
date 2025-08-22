-- Debug script for starred_items table issues
-- Run this in Supabase SQL Editor to diagnose the 406 errors

-- 1. Check current user authentication
SELECT 
    auth.uid() as current_user_id,
    auth.role() as current_role;

-- 2. Check table structure
\d starred_items;

-- 3. Check RLS status and policies
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE tablename = 'starred_items';

-- 4. List all policies on starred_items
SELECT 
    policyname,
    cmd as operation,
    permissive,
    roles,
    qual as using_expression,
    with_check as check_expression
FROM pg_policies 
WHERE tablename = 'starred_items'
ORDER BY cmd;

-- 5. Test basic table access (should work for authenticated users)
SELECT COUNT(*) as total_items FROM starred_items;

-- 6. Test specific query that's failing in the app
-- This simulates the exact query the app is trying to run
SELECT id FROM starred_items 
WHERE user_id = auth.uid() 
AND item_type = 'skill_node' 
AND item_id = 'test-id-12345'
LIMIT 1;

-- 7. Test insert capability
INSERT INTO starred_items (user_id, item_type, item_id, item_data)
VALUES (auth.uid(), 'skill_node', 'test-debug-item', '{"debug": true}')
ON CONFLICT (user_id, item_type, item_id) DO NOTHING;

-- 8. Verify the insert worked
SELECT * FROM starred_items 
WHERE user_id = auth.uid() 
AND item_type = 'skill_node' 
AND item_id = 'test-debug-item';

-- 9. Clean up test data
DELETE FROM starred_items 
WHERE user_id = auth.uid() 
AND item_type = 'skill_node' 
AND item_id = 'test-debug-item';

-- 10. Check for any foreign key constraints that might be causing issues
SELECT 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' 
AND tc.table_name='starred_items';

-- 11. Check if the API endpoint is properly exposed
-- This will show if the table is available via the PostgREST API
SELECT 
    table_name,
    is_insertable_into
FROM information_schema.tables 
WHERE table_name = 'starred_items' 
AND table_schema = 'public';