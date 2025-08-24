-- Find ALL foreign key constraints that reference skill_tree_nodes
SELECT 
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    a.attname AS column_name,
    confrelid::regclass AS foreign_table_name,
    af.attname AS foreign_column_name,
    pg_get_constraintdef(c.oid) AS constraint_definition
FROM 
    pg_constraint c
    JOIN pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
    JOIN pg_attribute af ON af.attnum = ANY(c.confkey) AND af.attrelid = c.confrelid
WHERE 
    c.contype = 'f'  -- foreign key constraints
    AND confrelid::regclass::text = 'skill_tree_nodes'
ORDER BY 
    conrelid::regclass::text, conname;

-- Also find columns that might reference skill_tree_nodes but don't have constraints
SELECT 
    table_name,
    column_name,
    data_type
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public'
    AND (
        column_name LIKE '%skill%' 
        OR column_name LIKE '%node%'
        OR column_name = 'parent_id'
        OR column_name = 'category_id'
        OR column_name = 'test_id'
    )
    AND table_name != 'skill_tree_nodes'
ORDER BY 
    table_name, column_name;