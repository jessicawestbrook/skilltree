-- ================================================
-- COURSE CONTENT SCHEMA
-- ================================================
-- This schema stores learning materials for each knowledge node
-- ================================================

-- Create course_content table
CREATE TABLE IF NOT EXISTS course_content (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  node_id VARCHAR(255) NOT NULL UNIQUE,
  title VARCHAR(255) NOT NULL,
  overview TEXT,
  learning_objectives JSONB DEFAULT '[]'::jsonb,
  estimated_time INTEGER DEFAULT 15, -- in minutes
  difficulty_level VARCHAR(20) DEFAULT 'beginner',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create course_sections table for organized content
CREATE TABLE IF NOT EXISTS course_sections (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content_id UUID REFERENCES course_content(id) ON DELETE CASCADE,
  section_order INTEGER NOT NULL,
  section_type VARCHAR(50) NOT NULL, -- 'introduction', 'concept', 'example', 'practice', 'summary'
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  media_url TEXT, -- for images, videos, etc.
  media_type VARCHAR(50), -- 'image', 'video', 'diagram', 'code'
  interactive_elements JSONB DEFAULT '[]'::jsonb, -- for interactive components
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create course_resources table for additional materials
CREATE TABLE IF NOT EXISTS course_resources (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content_id UUID REFERENCES course_content(id) ON DELETE CASCADE,
  resource_type VARCHAR(50) NOT NULL, -- 'video', 'article', 'exercise', 'documentation'
  title VARCHAR(255) NOT NULL,
  description TEXT,
  url TEXT,
  is_required BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create key_concepts table for important terms and definitions
CREATE TABLE IF NOT EXISTS key_concepts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content_id UUID REFERENCES course_content(id) ON DELETE CASCADE,
  term VARCHAR(255) NOT NULL,
  definition TEXT NOT NULL,
  example TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create learning_tips table for helpful hints
CREATE TABLE IF NOT EXISTS learning_tips (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content_id UUID REFERENCES course_content(id) ON DELETE CASCADE,
  tip_type VARCHAR(50) DEFAULT 'general', -- 'general', 'warning', 'best_practice', 'common_mistake'
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_course_content_node_id ON course_content(node_id);
CREATE INDEX IF NOT EXISTS idx_course_sections_content_id ON course_sections(content_id);
CREATE INDEX IF NOT EXISTS idx_course_sections_order ON course_sections(content_id, section_order);
CREATE INDEX IF NOT EXISTS idx_course_resources_content_id ON course_resources(content_id);
CREATE INDEX IF NOT EXISTS idx_key_concepts_content_id ON key_concepts(content_id);
CREATE INDEX IF NOT EXISTS idx_learning_tips_content_id ON learning_tips(content_id);

-- Enable Row Level Security
ALTER TABLE course_content ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE key_concepts ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_tips ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access
CREATE POLICY "Allow public read access to course content" ON course_content
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access to course sections" ON course_sections
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access to course resources" ON course_resources
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access to key concepts" ON key_concepts
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access to learning tips" ON learning_tips
  FOR SELECT TO public USING (true);

-- Add triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_course_content_updated_at 
  BEFORE UPDATE ON course_content 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();