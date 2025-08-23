-- Create user_flashcard_reviews table
CREATE TABLE IF NOT EXISTS user_flashcard_reviews (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  flashcard_id TEXT NOT NULL,
  flashcard_type TEXT NOT NULL CHECK (flashcard_type IN ('vocabulary', 'spelling', 'language', 'question', 'skill_node')),
  last_reviewed TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  next_review TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  review_count INTEGER NOT NULL DEFAULT 0,
  easiness_factor DECIMAL(3,2) NOT NULL DEFAULT 2.5 CHECK (easiness_factor >= 1.3 AND easiness_factor <= 2.5),
  interval_days INTEGER NOT NULL DEFAULT 0,
  consecutive_correct INTEGER NOT NULL DEFAULT 0,
  total_correct INTEGER NOT NULL DEFAULT 0,
  total_attempts INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, flashcard_id, flashcard_type)
);

-- Create flashcard_review_history table for analytics
CREATE TABLE IF NOT EXISTS flashcard_review_history (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  flashcard_id TEXT NOT NULL,
  flashcard_type TEXT NOT NULL CHECK (flashcard_type IN ('vocabulary', 'spelling', 'language', 'question', 'skill_node')),
  quality_rating INTEGER NOT NULL CHECK (quality_rating >= 0 AND quality_rating <= 5),
  time_taken_seconds INTEGER,
  hint_used BOOLEAN DEFAULT FALSE,
  next_interval_days INTEGER,
  reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_user_id ON user_flashcard_reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_next_review ON user_flashcard_reviews(next_review);
CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_type ON user_flashcard_reviews(flashcard_type);
CREATE INDEX IF NOT EXISTS idx_flashcard_review_history_user_id ON flashcard_review_history(user_id);
CREATE INDEX IF NOT EXISTS idx_flashcard_review_history_reviewed_at ON flashcard_review_history(reviewed_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for updated_at
DROP TRIGGER IF EXISTS update_user_flashcard_reviews_updated_at ON user_flashcard_reviews;
CREATE TRIGGER update_user_flashcard_reviews_updated_at
BEFORE UPDATE ON user_flashcard_reviews
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Enable RLS
ALTER TABLE user_flashcard_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE flashcard_review_history ENABLE ROW LEVEL SECURITY;

-- Policies for user_flashcard_reviews
DROP POLICY IF EXISTS "Users can view own flashcard reviews" ON user_flashcard_reviews;
CREATE POLICY "Users can view own flashcard reviews" ON user_flashcard_reviews
  FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own flashcard reviews" ON user_flashcard_reviews;
CREATE POLICY "Users can insert own flashcard reviews" ON user_flashcard_reviews
  FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own flashcard reviews" ON user_flashcard_reviews;
CREATE POLICY "Users can update own flashcard reviews" ON user_flashcard_reviews
  FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete own flashcard reviews" ON user_flashcard_reviews;
CREATE POLICY "Users can delete own flashcard reviews" ON user_flashcard_reviews
  FOR DELETE USING (auth.uid() = user_id);

-- Policies for flashcard_review_history
DROP POLICY IF EXISTS "Users can view own review history" ON flashcard_review_history;
CREATE POLICY "Users can view own review history" ON flashcard_review_history
  FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own review history" ON flashcard_review_history;
CREATE POLICY "Users can insert own review history" ON flashcard_review_history
  FOR INSERT WITH CHECK (auth.uid() = user_id);