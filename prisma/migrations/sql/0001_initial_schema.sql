-- Migration: initial_schema
-- Version: 0001
-- Date: 2024-01-01
-- Description: Create initial database schema

-- ============================================
-- Core Tables
-- ============================================

CREATE TABLE IF NOT EXISTS knowledge_nodes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  domain VARCHAR(100),
  category VARCHAR(100),
  difficulty INTEGER DEFAULT 1,
  points INTEGER DEFAULT 100,
  level INTEGER DEFAULT 0,
  is_parent BOOLEAN DEFAULT false,
  parent_id UUID REFERENCES knowledge_nodes(id),
  x FLOAT,
  y FLOAT,
  icon VARCHAR(100),
  is_available BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS node_prerequisites (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  node_id UUID NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  prerequisite_id UUID NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(node_id, prerequisite_id)
);

CREATE TABLE IF NOT EXISTS quiz_questions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  node_id UUID NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  question TEXT NOT NULL,
  options JSONB NOT NULL,
  correct INTEGER NOT NULL,
  explanation TEXT,
  difficulty INTEGER DEFAULT 1,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_knowledge_nodes_domain ON knowledge_nodes(domain);
CREATE INDEX idx_knowledge_nodes_category ON knowledge_nodes(category);
CREATE INDEX idx_knowledge_nodes_parent_id ON knowledge_nodes(parent_id);
CREATE INDEX idx_node_prerequisites_node_id ON node_prerequisites(node_id);
CREATE INDEX idx_node_prerequisites_prerequisite_id ON node_prerequisites(prerequisite_id);
CREATE INDEX idx_quiz_questions_node_id ON quiz_questions(node_id);