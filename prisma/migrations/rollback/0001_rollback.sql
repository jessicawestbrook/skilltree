-- Rollback for migration: initial_schema
-- Version: 0001

-- Drop indexes
DROP INDEX IF EXISTS idx_quiz_questions_node_id;
DROP INDEX IF EXISTS idx_node_prerequisites_prerequisite_id;
DROP INDEX IF EXISTS idx_node_prerequisites_node_id;
DROP INDEX IF EXISTS idx_knowledge_nodes_parent_id;
DROP INDEX IF EXISTS idx_knowledge_nodes_category;
DROP INDEX IF EXISTS idx_knowledge_nodes_domain;

-- Drop tables in reverse order
DROP TABLE IF EXISTS quiz_questions CASCADE;
DROP TABLE IF EXISTS node_prerequisites CASCADE;
DROP TABLE IF EXISTS knowledge_nodes CASCADE;