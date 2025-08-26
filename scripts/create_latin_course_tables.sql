-- Create tables for Latin course structure
-- These tables will support full course organization with chapters, sections, and learning content

-- 1. Create language_courses table
CREATE TABLE IF NOT EXISTS language_courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_id UUID NOT NULL REFERENCES languages(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    level VARCHAR(100),
    estimated_hours INTEGER,
    is_active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(language_id, name)
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_language_courses_language_id ON language_courses(language_id);
CREATE INDEX IF NOT EXISTS idx_language_courses_is_active ON language_courses(is_active);

-- 2. Create course_modules table (chapters/units)
CREATE TABLE IF NOT EXISTS course_modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES language_courses(id) ON DELETE CASCADE,
    parent_module_id UUID REFERENCES course_modules(id) ON DELETE CASCADE, -- For nested modules
    chapter_number INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    module_type VARCHAR(50) DEFAULT 'chapter', -- 'chapter', 'section', 'unit'
    display_order INTEGER DEFAULT 0,
    is_locked BOOLEAN DEFAULT false,
    prerequisites JSONB, -- Array of module IDs that must be completed first
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(course_id, chapter_number)
);

-- Create indexes for course_modules
CREATE INDEX IF NOT EXISTS idx_course_modules_course_id ON course_modules(course_id);
CREATE INDEX IF NOT EXISTS idx_course_modules_parent_id ON course_modules(parent_module_id);
CREATE INDEX IF NOT EXISTS idx_course_modules_display_order ON course_modules(display_order);

-- 3. Create module_content table (learning content within modules)
CREATE TABLE IF NOT EXISTS module_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id UUID NOT NULL REFERENCES course_modules(id) ON DELETE CASCADE,
    section_number INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    content_type VARCHAR(50) NOT NULL, -- 'lesson', 'explanation', 'example', 'vocabulary', 'grammar_rule'
    content JSONB NOT NULL, -- Flexible content structure
    display_order INTEGER DEFAULT 0,
    estimated_minutes INTEGER DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(module_id, section_number)
);

-- Create indexes for module_content
CREATE INDEX IF NOT EXISTS idx_module_content_module_id ON module_content(module_id);
CREATE INDEX IF NOT EXISTS idx_module_content_content_type ON module_content(content_type);
CREATE INDEX IF NOT EXISTS idx_module_content_display_order ON module_content(display_order);

-- 4. Create module_questions table (links questions to modules)
CREATE TABLE IF NOT EXISTS module_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id UUID NOT NULL REFERENCES course_modules(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES language_questions(id) ON DELETE CASCADE,
    section_number INTEGER, -- Which section this question belongs to
    display_order INTEGER DEFAULT 0,
    is_required BOOLEAN DEFAULT true, -- Whether this question must be answered to progress
    points INTEGER DEFAULT 10, -- Points awarded for correct answer
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(module_id, question_id)
);

-- Create indexes for module_questions
CREATE INDEX IF NOT EXISTS idx_module_questions_module_id ON module_questions(module_id);
CREATE INDEX IF NOT EXISTS idx_module_questions_question_id ON module_questions(question_id);
CREATE INDEX IF NOT EXISTS idx_module_questions_display_order ON module_questions(display_order);

-- 5. Create user_course_progress table
CREATE TABLE IF NOT EXISTS user_course_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES language_courses(id) ON DELETE CASCADE,
    current_module_id UUID REFERENCES course_modules(id),
    modules_completed INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, course_id)
);

-- Create indexes for user_course_progress
CREATE INDEX IF NOT EXISTS idx_user_course_progress_user_id ON user_course_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_course_progress_course_id ON user_course_progress(course_id);

-- 6. Create user_module_progress table
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
    UNIQUE(user_id, module_id)
);

-- Create indexes for user_module_progress
CREATE INDEX IF NOT EXISTS idx_user_module_progress_user_id ON user_module_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_module_progress_module_id ON user_module_progress(module_id);

-- 7. Create course_achievements table (optional gamification)
CREATE TABLE IF NOT EXISTS course_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES language_courses(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    icon_emoji VARCHAR(10),
    requirement_type VARCHAR(50), -- 'modules_completed', 'points_earned', 'perfect_score', etc.
    requirement_value INTEGER,
    points_awarded INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for course_achievements
CREATE INDEX IF NOT EXISTS idx_course_achievements_course_id ON course_achievements(course_id);

-- 8. Create user_course_achievements table
CREATE TABLE IF NOT EXISTS user_course_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    achievement_id UUID NOT NULL REFERENCES course_achievements(id) ON DELETE CASCADE,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);

-- Create indexes for user_course_achievements
CREATE INDEX IF NOT EXISTS idx_user_course_achievements_user_id ON user_course_achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_user_course_achievements_achievement_id ON user_course_achievements(achievement_id);

-- Add RLS policies for security
ALTER TABLE language_courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE module_content ENABLE ROW LEVEL SECURITY;
ALTER TABLE module_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_course_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_module_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_course_achievements ENABLE ROW LEVEL SECURITY;

-- Public read access for course content
CREATE POLICY "Course content is viewable by everyone" ON language_courses
    FOR SELECT USING (is_active = true);

CREATE POLICY "Course modules are viewable by everyone" ON course_modules
    FOR SELECT USING (true);

CREATE POLICY "Module content is viewable by everyone" ON module_content
    FOR SELECT USING (true);

CREATE POLICY "Module questions are viewable by everyone" ON module_questions
    FOR SELECT USING (true);

CREATE POLICY "Course achievements are viewable by everyone" ON course_achievements
    FOR SELECT USING (true);

-- User-specific progress policies
CREATE POLICY "Users can view their own course progress" ON user_course_progress
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own course progress" ON user_course_progress
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own course progress" ON user_course_progress
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own module progress" ON user_module_progress
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own module progress" ON user_module_progress
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own module progress" ON user_module_progress
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own achievements" ON user_course_achievements
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can earn achievements" ON user_course_achievements
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create update timestamp trigger function if it doesn't exist
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add update triggers for tables with updated_at
CREATE TRIGGER update_language_courses_updated_at BEFORE UPDATE ON language_courses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_course_modules_updated_at BEFORE UPDATE ON course_modules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_module_content_updated_at BEFORE UPDATE ON module_content
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add helpful comments
COMMENT ON TABLE language_courses IS 'Stores language courses with structured curriculum';
COMMENT ON TABLE course_modules IS 'Chapters and sections within a course';
COMMENT ON TABLE module_content IS 'Learning content (lessons, explanations) within modules';
COMMENT ON TABLE module_questions IS 'Links questions to specific course modules';
COMMENT ON TABLE user_course_progress IS 'Tracks user progress through entire courses';
COMMENT ON TABLE user_module_progress IS 'Tracks user progress through individual modules';
COMMENT ON TABLE course_achievements IS 'Gamification achievements for courses';
COMMENT ON TABLE user_course_achievements IS 'Achievements earned by users';