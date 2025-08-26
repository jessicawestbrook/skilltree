-- Complete slug migration for learning paths and courses
-- Run this entire script in Supabase SQL Editor

-- Step 1: Add slug columns
ALTER TABLE learning_paths 
ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

ALTER TABLE language_courses 
ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

-- Step 2: Create slug generation function
CREATE OR REPLACE FUNCTION generate_slug(input_text TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN LOWER(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    REGEXP_REPLACE(
                        TRIM(input_text),
                        '''', '', 'g'  -- Remove apostrophes
                    ),
                    '[^a-zA-Z0-9\s-]', '', 'g'  -- Remove special characters
                ),
                '\s+', '-', 'g'  -- Replace spaces with hyphens
            ),
            '-+', '-', 'g'  -- Replace multiple hyphens with single hyphen
        )
    );
END;
$$ LANGUAGE plpgsql;

-- Step 3: Update learning_paths with slugs
UPDATE learning_paths 
SET slug = generate_slug(name)
WHERE slug IS NULL;

-- Step 4: Update language_courses with slugs
UPDATE language_courses 
SET slug = generate_slug(name)
WHERE slug IS NULL;

-- Step 5: Handle any duplicates by adding numbers
WITH duplicates AS (
    SELECT slug, COUNT(*) as count
    FROM learning_paths
    WHERE slug IS NOT NULL
    GROUP BY slug
    HAVING COUNT(*) > 1
)
UPDATE learning_paths p1
SET slug = p1.slug || '-' || (
    SELECT COUNT(*)
    FROM learning_paths p2
    WHERE p2.slug = p1.slug
    AND p2.id < p1.id
) + 1
WHERE slug IN (SELECT slug FROM duplicates);

WITH duplicates AS (
    SELECT slug, COUNT(*) as count
    FROM language_courses
    WHERE slug IS NOT NULL
    GROUP BY slug
    HAVING COUNT(*) > 1
)
UPDATE language_courses c1
SET slug = c1.slug || '-' || (
    SELECT COUNT(*)
    FROM language_courses c2
    WHERE c2.slug = c1.slug
    AND c2.id < c1.id
) + 1
WHERE slug IN (SELECT slug FROM duplicates);

-- Step 6: Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_learning_paths_slug ON learning_paths(slug);
CREATE INDEX IF NOT EXISTS idx_language_courses_slug ON language_courses(slug);

-- Step 7: Add comments
COMMENT ON COLUMN learning_paths.slug IS 'URL-friendly identifier for the learning path';
COMMENT ON COLUMN language_courses.slug IS 'URL-friendly identifier for the course';

-- Step 8: Verify the results
SELECT 'Learning Paths:' as table_name, COUNT(*) as total, COUNT(slug) as with_slug 
FROM learning_paths
UNION ALL
SELECT 'Language Courses:' as table_name, COUNT(*) as total, COUNT(slug) as with_slug 
FROM language_courses;

-- Show sample URLs
SELECT 'Sample Learning Path URLs:' as info;
SELECT name, '/learning-paths/' || slug as url 
FROM learning_paths 
WHERE slug IS NOT NULL
LIMIT 3;

SELECT 'Sample Course URLs:' as info;
SELECT name, '/course/' || slug as url 
FROM language_courses 
WHERE slug IS NOT NULL
LIMIT 5;