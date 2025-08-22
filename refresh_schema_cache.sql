-- Force PostgREST to reload schema cache for user_bookmarks table
-- Run this in Supabase SQL Editor

-- 1. Refresh the PostgREST schema cache
NOTIFY pgrst, 'reload schema';

-- 2. Verify table exists in public schema
SELECT table_name, table_type 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('user_bookmarks', 'starred_items');

-- 3. Check table permissions
SELECT grantee, privilege_type
FROM information_schema.role_table_grants 
WHERE table_name = 'user_bookmarks' 
AND table_schema = 'public';

-- 4. Test basic access
SELECT COUNT(*) FROM user_bookmarks;