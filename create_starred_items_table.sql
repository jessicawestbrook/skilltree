-- Create starred_items table
CREATE TABLE IF NOT EXISTS starred_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  item_type VARCHAR(50) NOT NULL CHECK (item_type IN ('spelling_word', 'vocabulary_word', 'language_question', 'question', 'skill_node')),
  item_id VARCHAR(200) NOT NULL,
  item_data JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, item_type, item_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_starred_items_user_id ON starred_items(user_id);
CREATE INDEX IF NOT EXISTS idx_starred_items_type ON starred_items(item_type);
CREATE INDEX IF NOT EXISTS idx_starred_items_created_at ON starred_items(created_at);

-- Enable Row Level Security
ALTER TABLE starred_items ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view their own starred items" ON starred_items
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own starred items" ON starred_items
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own starred items" ON starred_items
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own starred items" ON starred_items
  FOR DELETE USING (auth.uid() = user_id);