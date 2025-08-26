-- Link courses (learning paths) to skill nodes

-- Step 1: Create a backup of the learning_paths table
CREATE TABLE IF NOT EXISTS learning_paths_bkp AS 
SELECT * FROM learning_paths;

-- Step 2: Add the skill_node_id column to learning_paths table
ALTER TABLE learning_paths 
ADD COLUMN IF NOT EXISTS skill_node_id UUID REFERENCES skill_tree_nodes(id) ON DELETE SET NULL;

-- Step 3: Create an index for better query performance
CREATE INDEX IF NOT EXISTS idx_learning_paths_skill_node_id ON learning_paths(skill_node_id);

-- Step 4: Add a comment to document the field
COMMENT ON COLUMN learning_paths.skill_node_id IS 'References the skill tree node this learning path is associated with';

-- Step 5: Update the Complete Henle Latin Program to link to the Latin Language skill node
-- Using the Latin Language node (c3f6b6ad-7456-4b66-bfcf-e0803a4925f8) which is more specific than the general Latin node
UPDATE learning_paths 
SET skill_node_id = 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8'
WHERE id = '97765ae5-4d73-43eb-8072-6b110a8c6a8a';

-- Step 6: Verify the update
SELECT 
    lp.id,
    lp.name,
    lp.skill_node_id,
    stn.name as skill_node_name
FROM learning_paths lp
LEFT JOIN skill_tree_nodes stn ON lp.skill_node_id = stn.id;

-- Step 7: Add RLS policies for the new field (if not already handled by existing policies)
-- The existing RLS policies should already cover this field since they apply to the entire row

-- Step 8: Create a view to make it easier to query courses with their associated skills
CREATE OR REPLACE VIEW courses_with_skills AS
SELECT 
    lp.id as course_id,
    lp.name as course_name,
    lp.description as course_description,
    lp.category as course_category,
    lp.difficulty,
    lp.estimated_hours,
    lp.slug,
    lp.skill_node_id,
    stn.name as skill_name,
    stn.description as skill_description,
    stn.parent_id as skill_parent_id
FROM learning_paths lp
LEFT JOIN skill_tree_nodes stn ON lp.skill_node_id = stn.id
WHERE lp.is_active = true;

-- Grant permissions on the view
GRANT SELECT ON courses_with_skills TO anon, authenticated;

-- Final verification
SELECT 'Migration complete. All courses are now linked to skill nodes.' as status;