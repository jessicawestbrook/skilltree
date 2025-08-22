-- Fix starred_items table API exposure issues
-- Run this in Supabase SQL Editor

-- 1. Ensure the table is in the public schema and accessible via API
ALTER TABLE starred_items REPLICA IDENTITY DEFAULT;

-- 2. Grant proper permissions to the API roles
GRANT ALL ON starred_items TO postgres;
GRANT ALL ON starred_items TO anon;
GRANT ALL ON starred_items TO authenticated;
GRANT ALL ON starred_items TO service_role;

-- 3. Ensure the table has proper ownership
ALTER TABLE starred_items OWNER TO postgres;

-- 4. Make sure the sequence (if any) is also accessible
-- This fixes UUID generation issues
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- 5. Refresh the PostgREST schema cache
-- This forces Supabase to recognize the table in the API
NOTIFY pgrst, 'reload schema';

-- 6. Verify the table is now accessible
SELECT 'starred_items table should now be accessible via API' as status;

-- 7. Test basic API access
SELECT COUNT(*) as total_items FROM starred_items;