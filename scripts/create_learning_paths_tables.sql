-- Create learning_paths table to store structured learning paths
CREATE TABLE IF NOT EXISTS learning_paths (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    difficulty VARCHAR(50), -- 'beginner', 'intermediate', 'advanced'
    estimated_hours INTEGER,
    icon_name VARCHAR(50), -- name of the icon to use
    color VARCHAR(50), -- color theme for the path
    language_id UUID REFERENCES languages(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    prerequisites JSONB DEFAULT '[]'::jsonb, -- Array of prerequisite path IDs
    metadata JSONB DEFAULT '{}'::jsonb, -- Additional metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(name)
);

-- Create learning_path_courses table to link courses to learning paths
CREATE TABLE IF NOT EXISTS learning_path_courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learning_path_id UUID NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES language_courses(id) ON DELETE CASCADE,
    sequence_number INTEGER NOT NULL, -- Order in the learning path
    is_required BOOLEAN DEFAULT true, -- Whether this course is required or optional
    unlock_after_course_id UUID REFERENCES language_courses(id), -- Previous course that must be completed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(learning_path_id, course_id),
    UNIQUE(learning_path_id, sequence_number)
);

-- Create user_learning_path_progress table
CREATE TABLE IF NOT EXISTS user_learning_path_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    learning_path_id UUID NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
    current_course_id UUID REFERENCES language_courses(id),
    courses_completed INTEGER DEFAULT 0,
    total_courses INTEGER DEFAULT 0,
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, learning_path_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_learning_paths_category ON learning_paths(category);
CREATE INDEX IF NOT EXISTS idx_learning_paths_is_active ON learning_paths(is_active);
CREATE INDEX IF NOT EXISTS idx_learning_paths_language_id ON learning_paths(language_id);
CREATE INDEX IF NOT EXISTS idx_learning_path_courses_path_id ON learning_path_courses(learning_path_id);
CREATE INDEX IF NOT EXISTS idx_learning_path_courses_course_id ON learning_path_courses(course_id);
CREATE INDEX IF NOT EXISTS idx_user_learning_path_progress_user_id ON user_learning_path_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_learning_path_progress_path_id ON user_learning_path_progress(learning_path_id);

-- Add RLS policies
ALTER TABLE learning_paths ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_path_courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_learning_path_progress ENABLE ROW LEVEL SECURITY;

-- Public read access for learning paths
CREATE POLICY "Learning paths are viewable by everyone" ON learning_paths
    FOR SELECT USING (is_active = true);

CREATE POLICY "Learning path courses are viewable by everyone" ON learning_path_courses
    FOR SELECT USING (true);

-- User-specific progress policies
CREATE POLICY "Users can view their own learning path progress" ON user_learning_path_progress
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own learning path progress" ON user_learning_path_progress
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own learning path progress" ON user_learning_path_progress
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Add update trigger for updated_at
CREATE TRIGGER update_learning_paths_updated_at BEFORE UPDATE ON learning_paths
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comments
COMMENT ON TABLE learning_paths IS 'Stores structured learning paths that group related courses';
COMMENT ON TABLE learning_path_courses IS 'Links courses to learning paths with sequence and requirements';
COMMENT ON TABLE user_learning_path_progress IS 'Tracks user progress through learning paths';