-- Add slug fields to learning_paths and language_courses tables

-- Add slug column to learning_paths
ALTER TABLE learning_paths 
ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

-- Add slug column to language_courses
ALTER TABLE language_courses 
ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

-- Create function to generate slug from text
CREATE OR REPLACE FUNCTION generate_slug(input_text TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN LOWER(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    TRIM(input_text),
                    '[^a-zA-Z0-9\s-]', '', 'g'  -- Remove special characters
                ),
                '\s+', '-', 'g'  -- Replace spaces with hyphens
            ),
            '-+', '-', 'g'  -- Replace multiple hyphens with single hyphen
        )
    );
END;
$$ LANGUAGE plpgsql;

-- Update existing learning_paths with slugs
UPDATE learning_paths 
SET slug = generate_slug(name)
WHERE slug IS NULL;

-- Update existing language_courses with slugs
UPDATE language_courses 
SET slug = generate_slug(name)
WHERE slug IS NULL;

-- Make slug columns NOT NULL after populating
ALTER TABLE learning_paths 
ALTER COLUMN slug SET NOT NULL;

ALTER TABLE language_courses 
ALTER COLUMN slug SET NOT NULL;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_learning_paths_slug ON learning_paths(slug);
CREATE INDEX IF NOT EXISTS idx_language_courses_slug ON language_courses(slug);

-- Add comments
COMMENT ON COLUMN learning_paths.slug IS 'URL-friendly identifier for the learning path';
COMMENT ON COLUMN language_courses.slug IS 'URL-friendly identifier for the course';

-- Verify the updates
SELECT 'Learning Paths with slugs:' as info;
SELECT name, slug FROM learning_paths LIMIT 5;

SELECT 'Language Courses with slugs:' as info;
SELECT name, slug FROM language_courses LIMIT 5;