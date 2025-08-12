-- Create quiz_questions table in Supabase
CREATE TABLE IF NOT EXISTS quiz_questions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  node_id VARCHAR(255) NOT NULL,
  question TEXT NOT NULL,
  options JSONB NOT NULL,
  correct_answer INTEGER NOT NULL,
  explanation TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_quiz_questions_node_id ON quiz_questions(node_id);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE quiz_questions ENABLE ROW LEVEL SECURITY;

-- Create policy to allow anyone to read questions (adjust as needed)
CREATE POLICY "Allow public read access" ON quiz_questions
  FOR SELECT
  TO public
  USING (true);

-- If you want to restrict writing to authenticated users only:
-- CREATE POLICY "Allow authenticated users to insert" ON quiz_questions
--   FOR INSERT
--   TO authenticated
--   WITH CHECK (true);

-- CREATE POLICY "Allow authenticated users to update" ON quiz_questions
--   FOR UPDATE
--   TO authenticated
--   USING (true)
--   WITH CHECK (true);

-- CREATE POLICY "Allow authenticated users to delete" ON quiz_questions
--   FOR DELETE
--   TO authenticated
--   USING (true);