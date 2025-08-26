
-- Add slug column to learning_paths
ALTER TABLE learning_paths 
ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

-- Add slug column to language_courses
ALTER TABLE language_courses 
ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_learning_paths_slug ON learning_paths(slug);
CREATE INDEX IF NOT EXISTS idx_language_courses_slug ON language_courses(slug);
