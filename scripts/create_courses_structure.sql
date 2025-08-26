-- Create proper course structure where each course is tied to a skill node
-- and learning paths can contain multiple courses from different skills

-- Step 1: Create backup of existing learning_paths table
CREATE TABLE IF NOT EXISTS learning_paths_bkp2 AS 
SELECT * FROM learning_paths;

-- Step 2: Create the courses table
CREATE TABLE IF NOT EXISTS courses (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    skill_node_id UUID NOT NULL REFERENCES skill_tree_nodes(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    slug VARCHAR(255) UNIQUE,
    difficulty VARCHAR(50) CHECK (difficulty IN ('beginner', 'intermediate', 'advanced', 'expert')),
    estimated_hours INTEGER,
    prerequisites JSONB DEFAULT '[]'::jsonb,
    learning_objectives JSONB DEFAULT '[]'::jsonb,
    content_modules JSONB DEFAULT '[]'::jsonb, -- Stores the course content structure
    metadata JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Step 3: Create indexes for courses
CREATE INDEX IF NOT EXISTS idx_courses_skill_node_id ON courses(skill_node_id);
CREATE INDEX IF NOT EXISTS idx_courses_slug ON courses(slug);
CREATE INDEX IF NOT EXISTS idx_courses_is_active ON courses(is_active);

-- Step 4: Create the learning_path_courses junction table
CREATE TABLE IF NOT EXISTS learning_path_courses (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    learning_path_id UUID NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    sequence_order INTEGER NOT NULL DEFAULT 0,
    is_required BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(learning_path_id, course_id)
);

-- Step 5: Create indexes for the junction table
CREATE INDEX IF NOT EXISTS idx_learning_path_courses_path_id ON learning_path_courses(learning_path_id);
CREATE INDEX IF NOT EXISTS idx_learning_path_courses_course_id ON learning_path_courses(course_id);

-- Step 6: Create user progress tracking for courses
CREATE TABLE IF NOT EXISTS user_course_progress (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    last_accessed TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, course_id)
);

-- Step 7: Create indexes for user progress
CREATE INDEX IF NOT EXISTS idx_user_course_progress_user_id ON user_course_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_course_progress_course_id ON user_course_progress(course_id);
CREATE INDEX IF NOT EXISTS idx_user_course_progress_status ON user_course_progress(status);

-- Step 8: Migrate the existing Henle Latin content to the new structure
-- First, create the Latin course tied to the Latin Language skill node
INSERT INTO courses (
    id,
    skill_node_id,
    name,
    description,
    slug,
    difficulty,
    estimated_hours,
    metadata,
    is_active
)
VALUES (
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a', -- Keep the same ID for consistency
    'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8', -- Latin Language skill node
    'Complete Henle Latin Program',
    'A comprehensive 4-year Latin curriculum based on the Henle textbook series',
    'complete-henle-latin-program',
    'intermediate',
    400, -- Estimated hours for full program
    '{"textbook": "Henle", "years": 4}'::jsonb,
    true
) ON CONFLICT (id) DO NOTHING;

-- Step 9: Link the course to the learning path
INSERT INTO learning_path_courses (
    learning_path_id,
    course_id,
    sequence_order,
    is_required
)
SELECT 
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a', -- Learning path ID
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a', -- Course ID (same as learning path for now)
    1,
    true
WHERE EXISTS (
    SELECT 1 FROM learning_paths WHERE id = '97765ae5-4d73-43eb-8072-6b110a8c6a8a'
)
ON CONFLICT (learning_path_id, course_id) DO NOTHING;

-- Step 10: Create helpful views
CREATE OR REPLACE VIEW learning_paths_with_courses AS
SELECT 
    lp.id as learning_path_id,
    lp.name as learning_path_name,
    lp.description as learning_path_description,
    lp.slug as learning_path_slug,
    lpc.sequence_order,
    lpc.is_required,
    c.id as course_id,
    c.name as course_name,
    c.description as course_description,
    c.skill_node_id,
    stn.name as skill_name,
    c.difficulty,
    c.estimated_hours
FROM learning_paths lp
JOIN learning_path_courses lpc ON lp.id = lpc.learning_path_id
JOIN courses c ON lpc.course_id = c.id
LEFT JOIN skill_tree_nodes stn ON c.skill_node_id = stn.id
WHERE lp.is_active = true AND c.is_active = true
ORDER BY lp.display_order, lpc.sequence_order;

-- Step 11: Create RLS policies for courses table
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;

-- Allow everyone to read active courses
CREATE POLICY "Courses are viewable by everyone" ON courses
    FOR SELECT USING (is_active = true);

-- Allow authenticated users to read all courses
CREATE POLICY "All courses viewable by authenticated users" ON courses
    FOR SELECT TO authenticated USING (true);

-- Allow admins to manage courses
CREATE POLICY "Admins can manage courses" ON courses
    FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.is_admin = true
        )
    );

-- Step 12: Create RLS policies for learning_path_courses
ALTER TABLE learning_path_courses ENABLE ROW LEVEL SECURITY;

-- Allow everyone to read
CREATE POLICY "Learning path courses viewable by everyone" ON learning_path_courses
    FOR SELECT USING (true);

-- Allow admins to manage
CREATE POLICY "Admins can manage learning path courses" ON learning_path_courses
    FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.is_admin = true
        )
    );

-- Step 13: Create RLS policies for user_course_progress
ALTER TABLE user_course_progress ENABLE ROW LEVEL SECURITY;

-- Users can view their own progress
CREATE POLICY "Users can view own course progress" ON user_course_progress
    FOR SELECT TO authenticated
    USING (user_id = auth.uid());

-- Users can update their own progress
CREATE POLICY "Users can update own course progress" ON user_course_progress
    FOR ALL TO authenticated
    USING (user_id = auth.uid());

-- Step 14: Grant permissions
GRANT SELECT ON courses TO anon, authenticated;
GRANT SELECT ON learning_path_courses TO anon, authenticated;
GRANT SELECT ON user_course_progress TO authenticated;
GRANT ALL ON courses TO authenticated;
GRANT ALL ON learning_path_courses TO authenticated;
GRANT ALL ON user_course_progress TO authenticated;
GRANT SELECT ON learning_paths_with_courses TO anon, authenticated;

-- Step 15: Add helpful comments
COMMENT ON TABLE courses IS 'Individual courses tied to specific skill nodes';
COMMENT ON TABLE learning_path_courses IS 'Junction table linking learning paths to multiple courses';
COMMENT ON TABLE user_course_progress IS 'Tracks user progress through individual courses';
COMMENT ON COLUMN courses.skill_node_id IS 'The skill tree node this course teaches';
COMMENT ON COLUMN courses.content_modules IS 'JSON structure defining the course modules, lessons, and content';

-- Verification query
SELECT 
    'Course structure created successfully. Courses are now tied to skill nodes.' as status,
    COUNT(*) as total_courses
FROM courses;