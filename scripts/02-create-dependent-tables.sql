-- ================================================
-- STEP 2: CREATE DEPENDENT TABLES
-- ================================================
-- Run this AFTER 01-create-core-tables.sql
-- Creates tables that depend on knowledge_nodes
-- ================================================

-- Now add the self-referencing foreign key to knowledge_nodes
DO $$
BEGIN
  -- Only add if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint 
    WHERE conname = 'knowledge_nodes_parent_id_fkey'
  ) THEN
    ALTER TABLE knowledge_nodes 
    ADD CONSTRAINT knowledge_nodes_parent_id_fkey 
    FOREIGN KEY (parent_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE;
  END IF;
END $$;

-- Create node_prerequisites table
CREATE TABLE IF NOT EXISTS node_prerequisites (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  node_id VARCHAR(255) NOT NULL,
  prerequisite_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  FOREIGN KEY (prerequisite_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  UNIQUE(node_id, prerequisite_id)
);

-- Create indexes for prerequisites
CREATE INDEX IF NOT EXISTS idx_node_prerequisites_node_id ON node_prerequisites(node_id);
CREATE INDEX IF NOT EXISTS idx_node_prerequisites_prerequisite_id ON node_prerequisites(prerequisite_id);

-- Create quiz_questions table
CREATE TABLE IF NOT EXISTS quiz_questions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  node_id VARCHAR(255) NOT NULL,
  question TEXT NOT NULL,
  options JSONB NOT NULL,
  correct_answer INTEGER NOT NULL,
  explanation TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE,
  
  FOREIGN KEY (node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE
);

-- Create index for quiz questions
CREATE INDEX IF NOT EXISTS idx_quiz_questions_node_id ON quiz_questions(node_id);

-- Create learning_path_nodes table
CREATE TABLE IF NOT EXISTS learning_path_nodes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  path_id UUID NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  order_index INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (path_id) REFERENCES learning_paths(id) ON DELETE CASCADE,
  FOREIGN KEY (node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  UNIQUE(path_id, node_id)
);

-- Create indexes for learning path nodes
CREATE INDEX IF NOT EXISTS idx_learning_path_nodes_path_id ON learning_path_nodes(path_id);
CREATE INDEX IF NOT EXISTS idx_learning_path_nodes_node_id ON learning_path_nodes(node_id);

-- Create user_progress table
CREATE TABLE IF NOT EXISTS user_progress (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL,
  node_id VARCHAR(255) NOT NULL,
  completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  points_earned INTEGER NOT NULL,
  quiz_score INTEGER,
  time_spent_seconds INTEGER,
  
  FOREIGN KEY (node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  UNIQUE(user_id, node_id)
);

-- Create indexes for user progress
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_node_id ON user_progress(node_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_completed_at ON user_progress(completed_at);

-- ================================================
-- Enable RLS on dependent tables
-- ================================================

ALTER TABLE node_prerequisites ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_path_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;

-- ================================================
-- Create policies for dependent tables
-- ================================================

-- Drop existing policies if they exist
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'node_prerequisites' 
    AND policyname = 'Allow public read access to prerequisites'
  ) THEN
    DROP POLICY "Allow public read access to prerequisites" ON node_prerequisites;
  END IF;
  
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'quiz_questions' 
    AND policyname = 'Allow public read access to questions'
  ) THEN
    DROP POLICY "Allow public read access to questions" ON quiz_questions;
  END IF;
  
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'learning_path_nodes' 
    AND policyname = 'Allow public read access to learning path nodes'
  ) THEN
    DROP POLICY "Allow public read access to learning path nodes" ON learning_path_nodes;
  END IF;
END $$;

-- Create policies
CREATE POLICY "Allow public read access to prerequisites" ON node_prerequisites
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access to questions" ON quiz_questions
  FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access to learning path nodes" ON learning_path_nodes
  FOR SELECT TO public USING (true);

-- User progress policies (authenticated only)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'user_progress' 
    AND policyname = 'Users can view own progress'
  ) THEN
    DROP POLICY "Users can view own progress" ON user_progress;
  END IF;
  
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'user_progress' 
    AND policyname = 'Users can insert own progress'
  ) THEN
    DROP POLICY "Users can insert own progress" ON user_progress;
  END IF;
  
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'user_progress' 
    AND policyname = 'Users can update own progress'
  ) THEN
    DROP POLICY "Users can update own progress" ON user_progress;
  END IF;
END $$;

CREATE POLICY "Users can view own progress" ON user_progress
  FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress" ON user_progress
  FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress" ON user_progress
  FOR UPDATE TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- User stats policies
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'user_stats' 
    AND policyname = 'Public can view leaderboard stats'
  ) THEN
    DROP POLICY "Public can view leaderboard stats" ON user_stats;
  END IF;
END $$;

CREATE POLICY "Public can view leaderboard stats" ON user_stats
  FOR SELECT TO public USING (true);

-- ================================================
-- Verification
-- ================================================

DO $$
BEGIN
  RAISE NOTICE 'Dependent tables created successfully!';
  RAISE NOTICE 'Tables created: node_prerequisites, quiz_questions, learning_path_nodes, user_progress';
  RAISE NOTICE 'Foreign key constraints added';
  RAISE NOTICE '';
  RAISE NOTICE 'Next: Run 03-create-user-tables.sql';
END $$;