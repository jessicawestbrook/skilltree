-- Create a new table with a different name to bypass API issues
-- Run this in Supabase SQL Editor

-- 1. Create table with a different name
CREATE TABLE user_bookmarks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    item_type TEXT NOT NULL CHECK (item_type IN ('spelling_word', 'vocabulary_word', 'language_question', 'question', 'skill_node')),
    item_id TEXT NOT NULL,
    item_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, item_type, item_id)
);

-- 2. Create indexes
CREATE INDEX idx_user_bookmarks_user_id ON user_bookmarks(user_id);
CREATE INDEX idx_user_bookmarks_type ON user_bookmarks(item_type);
CREATE INDEX idx_user_bookmarks_created_at ON user_bookmarks(created_at DESC);

-- 3. Enable RLS
ALTER TABLE user_bookmarks ENABLE ROW LEVEL SECURITY;

-- 4. Create RLS policies
CREATE POLICY "user_bookmarks_select" ON user_bookmarks
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "user_bookmarks_insert" ON user_bookmarks
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "user_bookmarks_update" ON user_bookmarks
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "user_bookmarks_delete" ON user_bookmarks
    FOR DELETE USING (auth.uid() = user_id);

-- 5. Grant permissions
GRANT ALL ON user_bookmarks TO postgres;
GRANT ALL ON user_bookmarks TO anon;
GRANT ALL ON user_bookmarks TO authenticated;
GRANT ALL ON user_bookmarks TO service_role;

-- 6. Test the new table
SELECT 'user_bookmarks table created successfully' as status;
SELECT COUNT(*) FROM user_bookmarks;