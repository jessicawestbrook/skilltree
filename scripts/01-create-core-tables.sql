-- ================================================
-- STEP 1: CREATE CORE TABLES FIRST
-- ================================================
-- Run this script FIRST to create the base tables
-- without foreign keys or dependencies
-- ================================================

-- Drop existing foreign key constraints if they exist (safe)
DO $$
BEGIN
  -- Drop foreign key from knowledge_nodes if it exists
  IF EXISTS (
    SELECT 1 FROM pg_constraint 
    WHERE conname = 'knowledge_nodes_parent_id_fkey'
  ) THEN
    ALTER TABLE knowledge_nodes DROP CONSTRAINT knowledge_nodes_parent_id_fkey;
  END IF;
END $$;

-- Create knowledge_nodes table WITHOUT foreign key to itself
CREATE TABLE IF NOT EXISTS knowledge_nodes (
  id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(100) NOT NULL,
  domain VARCHAR(100) NOT NULL,
  difficulty INTEGER NOT NULL CHECK (difficulty >= 1 AND difficulty <= 6),
  points INTEGER NOT NULL CHECK (points >= 0),
  level INTEGER DEFAULT 0,
  is_parent BOOLEAN DEFAULT false,
  parent_id VARCHAR(255), -- No foreign key yet
  position_x INTEGER,
  position_y INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for knowledge_nodes
CREATE INDEX IF NOT EXISTS idx_knowledge_nodes_category ON knowledge_nodes(category);
CREATE INDEX IF NOT EXISTS idx_knowledge_nodes_domain ON knowledge_nodes(domain);
CREATE INDEX IF NOT EXISTS idx_knowledge_nodes_parent_id ON knowledge_nodes(parent_id);

-- Create learning_paths table (no dependencies)
CREATE TABLE IF NOT EXISTS learning_paths (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  icon_name VARCHAR(100),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE
);

-- Create user_stats table (no dependencies)
CREATE TABLE IF NOT EXISTS user_stats (
  user_id UUID PRIMARY KEY,
  total_points INTEGER DEFAULT 0,
  neural_level INTEGER DEFAULT 1,
  memory_crystals INTEGER DEFAULT 0,
  synaptic_streak INTEGER DEFAULT 0,
  last_activity_date DATE,
  total_nodes_completed INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE
);

-- ================================================
-- Enable RLS on core tables
-- ================================================

ALTER TABLE knowledge_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_paths ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;

-- ================================================
-- Create basic policies
-- ================================================

-- Drop existing policies if they exist
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'knowledge_nodes' 
    AND policyname = 'Allow public read access to nodes'
  ) THEN
    DROP POLICY "Allow public read access to nodes" ON knowledge_nodes;
  END IF;
  
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'learning_paths' 
    AND policyname = 'Allow public read access to learning paths'
  ) THEN
    DROP POLICY "Allow public read access to learning paths" ON learning_paths;
  END IF;
END $$;

-- Create policies
CREATE POLICY "Allow public read access to nodes" ON knowledge_nodes
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access to learning paths" ON learning_paths
  FOR SELECT TO public USING (true);

-- ================================================
-- Verification
-- ================================================

DO $$
BEGIN
  RAISE NOTICE 'Core tables created successfully!';
  RAISE NOTICE 'Tables created: knowledge_nodes, learning_paths, user_stats';
  RAISE NOTICE '';
  RAISE NOTICE 'Next: Run 02-create-dependent-tables.sql';
END $$;