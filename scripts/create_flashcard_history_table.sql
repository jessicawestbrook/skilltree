-- Create flashcard_review_history table for analytics
CREATE TABLE IF NOT EXISTS flashcard_review_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    flashcard_id UUID NOT NULL,
    flashcard_type TEXT NOT NULL CHECK (flashcard_type IN ('vocabulary', 'spelling', 'language', 'question', 'skill_node')),
    quality_rating INTEGER NOT NULL CHECK (quality_rating >= 0 AND quality_rating <= 5),
    time_taken_seconds INTEGER,
    hint_used BOOLEAN DEFAULT FALSE,
    next_interval_days INTEGER,
    reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_flashcard_review_history_user_id ON flashcard_review_history(user_id);
CREATE INDEX IF NOT EXISTS idx_flashcard_review_history_flashcard ON flashcard_review_history(flashcard_id, flashcard_type);
CREATE INDEX IF NOT EXISTS idx_flashcard_review_history_reviewed_at ON flashcard_review_history(reviewed_at);

-- Enable Row Level Security
ALTER TABLE flashcard_review_history ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for flashcard_review_history
CREATE POLICY "Users can view their own review history" ON flashcard_review_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own review history" ON flashcard_review_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Note: No update or delete policies for history table as it should be append-only

-- Grant necessary permissions
GRANT ALL ON flashcard_review_history TO authenticated;
GRANT ALL ON flashcard_review_history TO anon;