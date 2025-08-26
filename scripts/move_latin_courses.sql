-- Move Henle Latin courses from "Latin Language" (under Roman Culture) to "Latin" (under Languages)
-- The Latin node under Languages has ID: b91a46fa-6e1e-48e0-acdd-4360393058b8

-- First, let's verify both nodes exist
DO $$
BEGIN
    -- Check that the target Latin node exists
    IF NOT EXISTS (
        SELECT 1 FROM skill_tree_nodes 
        WHERE id = 'b91a46fa-6e1e-48e0-acdd-4360393058b8'
        AND name = 'Latin'
    ) THEN
        RAISE EXCEPTION 'Target Latin node not found';
    END IF;
    
    -- Check that source courses exist
    IF NOT EXISTS (
        SELECT 1 FROM skill_tree_nodes 
        WHERE parent_id = 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8'
        AND name LIKE 'Henle Latin%'
    ) THEN
        RAISE EXCEPTION 'Henle Latin courses not found under Latin Language';
    END IF;
END $$;

-- Update the parent_id of all Henle Latin courses to point to the Latin node under Languages
UPDATE skill_tree_nodes
SET 
    parent_id = 'b91a46fa-6e1e-48e0-acdd-4360393058b8',  -- Latin under Languages
    updated_at = NOW()
WHERE 
    parent_id = 'c3f6b6ad-7456-4b66-bfcf-e0803a4925f8'  -- Latin Language under Roman Culture
    AND name LIKE 'Henle Latin%';

-- Adjust display_order to put courses after the existing Latin children
-- First, shift existing children's display_order up by 10 to make room
UPDATE skill_tree_nodes
SET display_order = display_order + 10
WHERE parent_id = 'b91a46fa-6e1e-48e0-acdd-4360393058b8'
AND name NOT LIKE 'Henle Latin%';

-- Now set the Henle courses to display_order 6-9 (after the 5 existing children)
UPDATE skill_tree_nodes SET display_order = 6 WHERE name = 'Henle Latin: First Year' AND parent_id = 'b91a46fa-6e1e-48e0-acdd-4360393058b8';
UPDATE skill_tree_nodes SET display_order = 7 WHERE name = 'Henle Latin: Second Year' AND parent_id = 'b91a46fa-6e1e-48e0-acdd-4360393058b8';
UPDATE skill_tree_nodes SET display_order = 8 WHERE name = 'Henle Latin: Third Year - Cicero' AND parent_id = 'b91a46fa-6e1e-48e0-acdd-4360393058b8';
UPDATE skill_tree_nodes SET display_order = 9 WHERE name = 'Henle Latin: Fourth Year - Virgil' AND parent_id = 'b91a46fa-6e1e-48e0-acdd-4360393058b8';

-- Verify the move
SELECT 
    'Moved courses to /languages/latin:' as message,
    COUNT(*) as course_count
FROM skill_tree_nodes
WHERE 
    parent_id = 'b91a46fa-6e1e-48e0-acdd-4360393058b8'
    AND name LIKE 'Henle Latin%';

-- Show all children of Latin node after the move
SELECT 
    name,
    display_order,
    CASE 
        WHEN metadata IS NOT NULL AND metadata::text != 'null' THEN 'Has metadata'
        ELSE 'No metadata'
    END as has_metadata
FROM skill_tree_nodes
WHERE parent_id = 'b91a46fa-6e1e-48e0-acdd-4360393058b8'
ORDER BY display_order, name;