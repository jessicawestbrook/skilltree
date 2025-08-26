-- Create user_module_progress table for tracking progress through course modules
CREATE TABLE IF NOT EXISTS user_module_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    module_id UUID NOT NULL REFERENCES course_modules(id) ON DELETE CASCADE,
    content_viewed JSONB DEFAULT '[]'::jsonb, -- Array of viewed content IDs
    questions_answered JSONB DEFAULT '[]'::jsonb, -- Array of answered question IDs
    questions_correct INTEGER DEFAULT 0,
    questions_total INTEGER DEFAULT 0,
    points_earned INTEGER DEFAULT 0,
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, module_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_module_progress_user_id ON user_module_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_module_progress_module_id ON user_module_progress(module_id);
CREATE INDEX IF NOT EXISTS idx_user_module_progress_completion ON user_module_progress(completion_percentage);

-- Enable Row Level Security
ALTER TABLE user_module_progress ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Users can update their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Users can insert their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Users can delete their own module progress" ON user_module_progress;

-- Create RLS policies
-- Users can only see their own progress
CREATE POLICY "Users can view their own module progress" ON user_module_progress
    FOR SELECT USING (auth.uid() = user_id);

-- Users can only update their own progress
CREATE POLICY "Users can update their own module progress" ON user_module_progress
    FOR UPDATE USING (auth.uid() = user_id);

-- Users can only insert their own progress
CREATE POLICY "Users can insert their own module progress" ON user_module_progress
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can delete their own progress (for reset functionality)
CREATE POLICY "Users can delete their own module progress" ON user_module_progress
    FOR DELETE USING (auth.uid() = user_id);

-- Create update trigger for last_accessed_at
CREATE OR REPLACE FUNCTION update_last_accessed_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_accessed_at = NOW();
    -- Also check if module is completed
    IF NEW.completion_percentage >= 100 AND OLD.completion_percentage < 100 THEN
        NEW.completed_at = NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop trigger if exists and create new one
DROP TRIGGER IF EXISTS update_user_module_progress_last_accessed ON user_module_progress;
CREATE TRIGGER update_user_module_progress_last_accessed
    BEFORE UPDATE ON user_module_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_last_accessed_at();

-- Add helpful comments
COMMENT ON TABLE user_module_progress IS 'Tracks individual user progress through course modules';
COMMENT ON COLUMN user_module_progress.content_viewed IS 'JSON array of content section IDs that have been viewed';
COMMENT ON COLUMN user_module_progress.questions_answered IS 'JSON array of question IDs that have been answered';
COMMENT ON COLUMN user_module_progress.questions_correct IS 'Number of questions answered correctly';
COMMENT ON COLUMN user_module_progress.points_earned IS 'Total points earned in this module';
COMMENT ON COLUMN user_module_progress.completion_percentage IS 'Percentage of module completed (0-100)';

-- Create a view for easy progress reporting
CREATE OR REPLACE VIEW user_module_progress_summary AS
SELECT 
    ump.*,
    p.username,
    p.full_name,
    cm.title as module_title,
    cm.chapter_number,
    lc.name as course_name,
    l.name as language_name
FROM user_module_progress ump
JOIN profiles p ON ump.user_id = p.id
JOIN course_modules cm ON ump.module_id = cm.id
JOIN language_courses lc ON cm.course_id = lc.id
LEFT JOIN languages l ON lc.language_id = l.id;

-- Grant access to the view
GRANT SELECT ON user_module_progress_summary TO authenticated;

-- Sample query to check user progress
-- SELECT * FROM user_module_progress WHERE user_id = auth.uid();

-- Sample query to get progress summary
-- SELECT 
--     module_title,
--     course_name,
--     completion_percentage,
--     questions_correct || '/' || questions_total as score,
--     started_at,
--     completed_at
-- FROM user_module_progress_summary 
-- WHERE user_id = auth.uid()
-- ORDER BY last_accessed_at DESC;