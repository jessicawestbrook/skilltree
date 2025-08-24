-- Check all views in the database and their dependencies
SELECT 
    viewname AS view_name,
    schemaname AS schema,
    definition
FROM pg_views
WHERE schemaname = 'public'
ORDER BY viewname;

-- Check dependencies for skill_tree_nodes table
SELECT DISTINCT
    dependent_ns.nspname AS dependent_schema,
    dependent_view.relname AS dependent_view,
    source_ns.nspname AS source_schema,
    source_table.relname AS source_table
FROM pg_depend 
JOIN pg_rewrite ON pg_depend.objid = pg_rewrite.oid 
JOIN pg_class AS dependent_view ON pg_rewrite.ev_class = dependent_view.oid 
JOIN pg_class AS source_table ON pg_depend.refobjid = source_table.oid 
JOIN pg_namespace dependent_ns ON dependent_view.relnamespace = dependent_ns.oid
JOIN pg_namespace source_ns ON source_table.relnamespace = source_ns.oid
WHERE 
    source_ns.nspname = 'public'
    AND source_table.relname = 'skill_tree_nodes'
    AND dependent_view.relkind = 'v'
ORDER BY dependent_view.relname;

-- Get the exact definition of skill_nodes_with_content_and_questions view
SELECT pg_get_viewdef('skill_nodes_with_content_and_questions'::regclass, true) AS view_definition;