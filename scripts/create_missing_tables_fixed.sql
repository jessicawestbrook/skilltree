-- Fixed SQL script to create missing database tables
-- This version handles existing tables and different column names

-- 1. Create notifications table (only if it doesn't exist)
CREATE TABLE IF NOT EXISTS notifications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('achievement', 'progress', 'reminder', 'system', 'social')),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    data JSONB,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

-- 2. Create notification_preferences table (only if it doesn't exist)
CREATE TABLE IF NOT EXISTS notification_preferences (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email_notifications BOOLEAN DEFAULT TRUE,
    push_notifications BOOLEAN DEFAULT TRUE,
    achievement_notifications BOOLEAN DEFAULT TRUE,
    progress_notifications BOOLEAN DEFAULT TRUE,
    reminder_notifications BOOLEAN DEFAULT TRUE,
    system_notifications BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Handle user_progress table - check if it exists first
DO $$
BEGIN
    -- Check if user_progress table exists
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_progress') THEN
        -- Table exists, check if skill_node_id column exists
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user_progress' AND column_name = 'skill_node_id') THEN
            -- Add skill_node_id column if it doesn't exist
            ALTER TABLE user_progress ADD COLUMN skill_node_id TEXT;
        END IF;
        
        -- Ensure other required columns exist
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user_progress' AND column_name = 'status') THEN
            ALTER TABLE user_progress ADD COLUMN status TEXT DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed'));
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user_progress' AND column_name = 'rating') THEN
            ALTER TABLE user_progress ADD COLUMN rating INTEGER DEFAULT 0 CHECK (rating >= 0 AND rating <= 100);
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user_progress' AND column_name = 'last_accessed') THEN
            ALTER TABLE user_progress ADD COLUMN last_accessed TIMESTAMPTZ DEFAULT NOW();
        END IF;
        
    ELSE
        -- Create user_progress table from scratch
        CREATE TABLE user_progress (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
            skill_node_id TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('not_started', 'in_progress', 'completed')) DEFAULT 'not_started',
            rating INTEGER DEFAULT 0 CHECK (rating >= 0 AND rating <= 100),
            last_accessed TIMESTAMPTZ DEFAULT NOW(),
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(user_id, skill_node_id)
        );
    END IF;
END $$;

-- 4. Handle starred_items table
DO $$
BEGIN
    -- Check if starred_items table exists
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'starred_items') THEN
        -- Ensure required columns exist
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'starred_items' AND column_name = 'item_type') THEN
            ALTER TABLE starred_items ADD COLUMN item_type TEXT CHECK (item_type IN ('spelling_word', 'vocabulary_word', 'language_question', 'question', 'skill_node'));
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'starred_items' AND column_name = 'item_id') THEN
            ALTER TABLE starred_items ADD COLUMN item_id TEXT;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'starred_items' AND column_name = 'item_data') THEN
            ALTER TABLE starred_items ADD COLUMN item_data JSONB;
        END IF;
        
    ELSE
        -- Create starred_items table from scratch
        CREATE TABLE starred_items (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
            item_type TEXT NOT NULL CHECK (item_type IN ('spelling_word', 'vocabulary_word', 'language_question', 'question', 'skill_node')),
            item_id TEXT NOT NULL,
            item_data JSONB,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(user_id, item_type, item_id)
        );
    END IF;
END $$;

-- 5. Create indexes (only if they don't exist)
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notifications_expires_at ON notifications(expires_at);

CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_skill_node ON user_progress(skill_node_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_last_accessed ON user_progress(last_accessed DESC);

CREATE INDEX IF NOT EXISTS idx_starred_items_user_id ON starred_items(user_id);
CREATE INDEX IF NOT EXISTS idx_starred_items_type ON starred_items(item_type);
CREATE INDEX IF NOT EXISTS idx_starred_items_created_at ON starred_items(created_at DESC);

-- 6. Enable Row Level Security (only if not already enabled)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'notifications' AND rowsecurity = true) THEN
        ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'notification_preferences' AND rowsecurity = true) THEN
        ALTER TABLE notification_preferences ENABLE ROW LEVEL SECURITY;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'user_progress' AND rowsecurity = true) THEN
        ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'starred_items' AND rowsecurity = true) THEN
        ALTER TABLE starred_items ENABLE ROW LEVEL SECURITY;
    END IF;
END $$;

-- 7. Create RLS policies (with IF NOT EXISTS equivalent using exception handling)
-- Notifications policies
DO $$
BEGIN
    CREATE POLICY "Users can view their own notifications" ON notifications
        FOR SELECT USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;  -- Policy already exists
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can insert their own notifications" ON notifications
        FOR INSERT WITH CHECK (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can update their own notifications" ON notifications
        FOR UPDATE USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can delete their own notifications" ON notifications
        FOR DELETE USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

-- Notification preferences policies
DO $$
BEGIN
    CREATE POLICY "Users can view their own notification preferences" ON notification_preferences
        FOR SELECT USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can insert their own notification preferences" ON notification_preferences
        FOR INSERT WITH CHECK (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can update their own notification preferences" ON notification_preferences
        FOR UPDATE USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

-- User progress policies
DO $$
BEGIN
    CREATE POLICY "Users can view their own progress" ON user_progress
        FOR SELECT USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can insert their own progress" ON user_progress
        FOR INSERT WITH CHECK (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can update their own progress" ON user_progress
        FOR UPDATE USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can delete their own progress" ON user_progress
        FOR DELETE USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

-- Starred items policies
DO $$
BEGIN
    CREATE POLICY "Users can view their own starred items" ON starred_items
        FOR SELECT USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can insert their own starred items" ON starred_items
        FOR INSERT WITH CHECK (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can update their own starred items" ON starred_items
        FOR UPDATE USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    CREATE POLICY "Users can delete their own starred items" ON starred_items
        FOR DELETE USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

-- 8. Create trigger function (only if it doesn't exist)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 9. Create triggers (with conditional creation)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_notification_preferences_updated_at') THEN
        CREATE TRIGGER update_notification_preferences_updated_at 
            BEFORE UPDATE ON notification_preferences 
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_user_progress_updated_at') THEN
        CREATE TRIGGER update_user_progress_updated_at 
            BEFORE UPDATE ON user_progress 
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    END IF;
END $$;

-- 10. Insert default notification preferences for existing users
INSERT INTO notification_preferences (user_id)
SELECT id FROM auth.users 
WHERE id NOT IN (SELECT user_id FROM notification_preferences)
ON CONFLICT (user_id) DO NOTHING;

-- Final verification
SELECT 'Tables created successfully!' as status;
SELECT table_name, 
       (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
AND table_name IN ('notifications', 'notification_preferences', 'user_progress', 'starred_items')
ORDER BY table_name;