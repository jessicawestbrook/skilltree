-- Fix the Latin course structure using skill_tree_nodes
-- Courses are skill_tree_nodes with their parent_id pointing to a skill

-- Step 1: Create course nodes under the Latin Language skill
-- Latin Language skill node ID: c3f6b6ad-7456-4b66-bfcf-e0803a4925f8

-- Create Henle Latin Year 1 course node
INSERT INTO skill_tree_nodes (
    id,
    parent_id,
    name,
    description,
    display_order,
    metadata,
    is_hidden
) VALUES (
    'cebb7f42-e51b-4ac4-8464-29fee0894024', -- Use the existing ID from learning_path_courses
    'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8', -- Latin Language skill
    'Henle Latin: First Year',
    'First year of the comprehensive Henle Latin program. Covers basic Latin grammar, vocabulary, and introduces students to reading simple Latin texts. Topics include the five declensions, basic verb conjugations, and fundamental syntax.',
    1,
    '{"textbook": "Henle First Year Latin", "year": 1, "chapters": 36}'::jsonb,
    false
) ON CONFLICT (id) DO UPDATE SET
    parent_id = EXCLUDED.parent_id,
    name = EXCLUDED.name,
    description = EXCLUDED.description;

-- Create Henle Latin Year 2 course node
INSERT INTO skill_tree_nodes (
    id,
    parent_id,
    name,
    description,
    display_order,
    metadata,
    is_hidden
) VALUES (
    'b1661d5c-7e1f-44a9-bbb4-17265e521670', -- Use the existing ID from learning_path_courses
    'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8', -- Latin Language skill
    'Henle Latin: Second Year',
    'Second year of the Henle Latin program. Continues grammar study with more complex constructions, introduces subjunctive mood, and begins reading Caesar''s Gallic Wars. Expands vocabulary and deepens understanding of Roman culture.',
    2,
    '{"textbook": "Henle Second Year Latin", "year": 2, "primary_text": "Caesar"}'::jsonb,
    false
) ON CONFLICT (id) DO UPDATE SET
    parent_id = EXCLUDED.parent_id,
    name = EXCLUDED.name,
    description = EXCLUDED.description;

-- Create Henle Latin Year 3 course node
INSERT INTO skill_tree_nodes (
    id,
    parent_id,
    name,
    description,
    display_order,
    metadata,
    is_hidden
) VALUES (
    'b72b43fa-c306-40da-b7a1-bfd46990cb80', -- Use the existing ID from learning_path_courses
    'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8', -- Latin Language skill
    'Henle Latin: Third Year - Cicero',
    'Third year focuses on reading Cicero''s orations and letters. Students analyze rhetorical techniques, advanced grammar, and the historical context of the late Roman Republic. Develops skills in literary analysis and translation.',
    3,
    '{"textbook": "Henle Third Year Latin", "year": 3, "primary_author": "Cicero"}'::jsonb,
    false
) ON CONFLICT (id) DO UPDATE SET
    parent_id = EXCLUDED.parent_id,
    name = EXCLUDED.name,
    description = EXCLUDED.description;

-- Create Henle Latin Year 4 course node (adding new ones for completeness)
INSERT INTO skill_tree_nodes (
    id,
    parent_id,
    name,
    description,
    display_order,
    metadata,
    is_hidden
) VALUES (
    gen_random_uuid(),
    'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8', -- Latin Language skill
    'Henle Latin: Fourth Year - Virgil',
    'Fourth year focuses on Virgil''s Aeneid. Students read extensive passages from the epic, studying poetic devices, meter (dactylic hexameter), and the literary and cultural significance of Rome''s national epic.',
    4,
    '{"textbook": "Henle Fourth Year Latin", "year": 4, "primary_text": "Aeneid"}'::jsonb,
    false
) ON CONFLICT DO NOTHING;

-- Step 2: Add the fourth year course to the learning path
INSERT INTO learning_path_courses (
    learning_path_id,
    course_id,
    sequence_number,
    is_required,
    unlock_after_course_id
)
SELECT 
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a', -- Learning path ID
    id, -- The new Year 4 course ID
    4,
    true,
    'b72b43fa-c306-40da-b7a1-bfd46990cb80' -- Unlock after Year 3
FROM skill_tree_nodes
WHERE name = 'Henle Latin: Fourth Year - Virgil'
AND parent_id = 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8'
ON CONFLICT DO NOTHING;

-- Step 3: Verify the structure
SELECT 
    'Verification: Course nodes created under Latin Language skill' as status,
    stn.name as course_name,
    stn.display_order,
    parent.name as skill_name,
    lpc.sequence_number as path_sequence
FROM skill_tree_nodes stn
JOIN skill_tree_nodes parent ON stn.parent_id = parent.id
LEFT JOIN learning_path_courses lpc ON lpc.course_id = stn.id
WHERE stn.parent_id = 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8'
ORDER BY stn.display_order;

-- Step 4: Create a helpful view for courses
CREATE OR REPLACE VIEW courses_view AS
SELECT 
    course.id as course_id,
    course.name as course_name,
    course.description as course_description,
    course.display_order as course_order,
    course.metadata as course_metadata,
    skill.id as skill_id,
    skill.name as skill_name,
    category.id as category_id,
    category.name as category_name
FROM skill_tree_nodes course
JOIN skill_tree_nodes skill ON course.parent_id = skill.id
LEFT JOIN skill_tree_nodes category ON skill.parent_id = category.id
WHERE course.parent_id IS NOT NULL  -- Has a parent (is a course)
  AND skill.parent_id IS NOT NULL    -- Parent also has a parent (confirms it's a skill)
  AND course.is_hidden = false;

-- Grant permissions
GRANT SELECT ON courses_view TO anon, authenticated;

-- Final message
SELECT 
    'SUCCESS: Latin courses are now properly set up as skill_tree_nodes' as message,
    'Each course has parent_id = skill node ID' as structure,
    COUNT(*) as total_courses
FROM skill_tree_nodes
WHERE parent_id = 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8';