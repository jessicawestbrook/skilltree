-- Final script to create user_bookmarks table
-- IMPORTANT: Run this in Supabase SQL Editor to resolve 404 errors

-- 1. Drop existing table if it exists
DROP TABLE IF EXISTS user_bookmarks CASCADE;

-- 2. Create the user_bookmarks table from scratch
CREATE TABLE user_bookmarks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    item_type TEXT NOT NULL CHECK (item_type IN ('spelling_word', 'vocabulary_word', 'language_question', 'question', 'skill_node')),
    item_id TEXT NOT NULL,
    item_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, item_type, item_id)
);

-- 3. Set proper ownership
ALTER TABLE user_bookmarks OWNER TO postgres;

-- 4. Create indexes for performance
CREATE INDEX idx_user_bookmarks_user_id ON user_bookmarks(user_id);
CREATE INDEX idx_user_bookmarks_type ON user_bookmarks(item_type);
CREATE INDEX idx_user_bookmarks_created_at ON user_bookmarks(created_at DESC);

-- 5. Enable Row Level Security
ALTER TABLE user_bookmarks ENABLE ROW LEVEL SECURITY;

-- 6. Create RLS policies for security
CREATE POLICY "user_bookmarks_select" ON user_bookmarks
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "user_bookmarks_insert" ON user_bookmarks
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "user_bookmarks_update" ON user_bookmarks
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "user_bookmarks_delete" ON user_bookmarks
    FOR DELETE USING (auth.uid() = user_id);

-- 7. Grant all necessary permissions to make table accessible via API
GRANT ALL ON user_bookmarks TO postgres;
GRANT ALL ON user_bookmarks TO anon;
GRANT ALL ON user_bookmarks TO authenticated;
GRANT ALL ON user_bookmarks TO service_role;

-- 8. Grant sequence permissions for UUID generation
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO service_role;

-- 9. Force PostgREST to reload its schema cache (critical!)
NOTIFY pgrst, 'reload schema';

-- 10. Test the table creation
SELECT 'user_bookmarks table created and configured successfully' as status;

-- 11. Verify the table structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'user_bookmarks' 
ORDER BY ordinal_position;

-- 12. Test basic API access (should return 0 rows but no error)
SELECT COUNT(*) FROM user_bookmarks;