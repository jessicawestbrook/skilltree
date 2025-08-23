-- Check if starred_items table exists and has data
SELECT COUNT(*) as total_starred_items FROM starred_items;

-- Check starred items for your user (replace with your actual user_id)
SELECT * FROM starred_items 
WHERE user_id = '5876bd4e-5e68-4b4d-be15-8f0171bfae93'
ORDER BY created_at DESC;

-- If you need to create some test starred items, uncomment and run:
-- INSERT INTO starred_items (user_id, item_type, item_id, created_at)
-- VALUES 
--   ('5876bd4e-5e68-4b4d-be15-8f0171bfae93', 'skill_node', '00000000-0000-0000-0000-000000000001', NOW()),
--   ('5876bd4e-5e68-4b4d-be15-8f0171bfae93', 'skill_node', '00000000-0000-0000-0000-000000000002', NOW()),
--   ('5876bd4e-5e68-4b4d-be15-8f0171bfae93', 'skill_node', '00000000-0000-0000-0000-000000000003', NOW())
-- ON CONFLICT DO NOTHING;

-- Get some sample skill_tree_nodes IDs to star
SELECT id, name, learning_area 
FROM skill_tree_nodes 
WHERE has_learning_content = true
LIMIT 10;