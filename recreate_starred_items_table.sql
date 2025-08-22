-- Completely recreate starred_items table with proper API exposure
-- Run this in Supabase SQL Editor

-- 1. Drop the existing table completely
DROP TABLE IF EXISTS starred_items CASCADE;

-- 2. Create the table from scratch with proper configuration
CREATE TABLE starred_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    item_type TEXT NOT NULL CHECK (item_type IN ('spelling_word', 'vocabulary_word', 'language_question', 'question', 'skill_node')),
    item_id TEXT NOT NULL,
    item_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, item_type, item_id)
);

-- 3. Set proper ownership
ALTER TABLE starred_items OWNER TO postgres;

-- 4. Create indexes
CREATE INDEX idx_starred_items_user_id ON starred_items(user_id);
CREATE INDEX idx_starred_items_type ON starred_items(item_type);
CREATE INDEX idx_starred_items_created_at ON starred_items(created_at DESC);

-- 5. Enable RLS
ALTER TABLE starred_items ENABLE ROW LEVEL SECURITY;

-- 6. Create RLS policies
CREATE POLICY "starred_items_select" ON starred_items
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "starred_items_insert" ON starred_items
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "starred_items_update" ON starred_items
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "starred_items_delete" ON starred_items
    FOR DELETE USING (auth.uid() = user_id);

-- 7. Grant permissions to all necessary roles
GRANT ALL ON starred_items TO postgres;
GRANT ALL ON starred_items TO anon;
GRANT ALL ON starred_items TO authenticated;
GRANT ALL ON starred_items TO service_role;

-- 8. Ensure sequences are accessible
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO service_role;

-- 9. Force PostgREST to reload schema
NOTIFY pgrst, 'reload schema';

-- 10. Test basic access
SELECT 'starred_items table recreated successfully' as status;

-- 11. Verify structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'starred_items' 
ORDER BY ordinal_position;

-- 12. Test API access (this should work without errors)
SELECT COUNT(*) FROM starred_items;