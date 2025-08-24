-- Create user_flashcard_reviews table for spaced repetition
CREATE TABLE IF NOT EXISTS public.user_flashcard_reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  flashcard_id TEXT NOT NULL,
  flashcard_type TEXT NOT NULL CHECK (flashcard_type IN ('vocabulary', 'spelling', 'language', 'question', 'skill_node')),
  
  -- Review tracking
  review_count INTEGER DEFAULT 0,
  correct_count INTEGER DEFAULT 0,
  incorrect_count INTEGER DEFAULT 0,
  
  -- Spaced repetition fields
  ease_factor NUMERIC(3,2) DEFAULT 2.5,
  interval_days INTEGER DEFAULT 0,
  next_review TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_reviewed TIMESTAMP WITH TIME ZONE,
  
  -- Performance tracking
  average_response_time INTEGER, -- in seconds
  last_response_time INTEGER, -- in seconds
  
  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT unique_user_flashcard UNIQUE (user_id, flashcard_id, flashcard_type)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_user_id ON public.user_flashcard_reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_next_review ON public.user_flashcard_reviews(next_review);
CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_flashcard_type ON public.user_flashcard_reviews(flashcard_type);

-- Enable Row Level Security
ALTER TABLE public.user_flashcard_reviews ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS
-- Users can only see their own reviews
CREATE POLICY "Users can view own flashcard reviews" ON public.user_flashcard_reviews
  FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own reviews
CREATE POLICY "Users can insert own flashcard reviews" ON public.user_flashcard_reviews
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own reviews
CREATE POLICY "Users can update own flashcard reviews" ON public.user_flashcard_reviews
  FOR UPDATE USING (auth.uid() = user_id);

-- Users can delete their own reviews
CREATE POLICY "Users can delete own flashcard reviews" ON public.user_flashcard_reviews
  FOR DELETE USING (auth.uid() = user_id);

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_flashcard_reviews_updated_at
  BEFORE UPDATE ON public.user_flashcard_reviews
  FOR EACH ROW
  EXECUTE FUNCTION public.update_updated_at_column();