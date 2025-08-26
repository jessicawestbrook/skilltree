-- Create news_items table for managing site news and updates
CREATE TABLE IF NOT EXISTS news_items (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  icon_name VARCHAR(50), -- Name of the Heroicon to use
  link VARCHAR(500), -- Optional link URL
  link_text VARCHAR(100), -- Optional link button text
  date_posted DATE DEFAULT CURRENT_DATE,
  is_published BOOLEAN DEFAULT true,
  display_order INTEGER DEFAULT 0, -- Lower numbers display first
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  created_by UUID REFERENCES auth.users(id)
);

-- Create index for faster queries
CREATE INDEX idx_news_items_published_order ON news_items(is_published, display_order, date_posted DESC);

-- Enable RLS
ALTER TABLE news_items ENABLE ROW LEVEL SECURITY;

-- Policy for reading news items (anyone can read published items)
CREATE POLICY "Anyone can read published news items" ON news_items
  FOR SELECT
  USING (is_published = true);

-- Policy for admins to manage news items
CREATE POLICY "Admins can manage news items" ON news_items
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.is_admin = true
    )
  );

-- Insert initial news items
INSERT INTO news_items (title, description, icon_name, link, link_text, date_posted, display_order) VALUES
  ('Scripps Spelling Bee Study Lists Added', 
   'Master spelling with official Scripps National Spelling Bee word lists, now available in our spelling and vocabulary flashcards.',
   'SparklesIcon',
   '/spelling-bee?tab=spelling',
   'Start Practicing',
   '2025-08-01',
   1),
  ('35,000 Spanish Vocabulary Words',
   'Comprehensive Spanish vocabulary flashcards covering the most common words from beginner to advanced levels.',
   'BookOpenIcon',
   '/language-trainer?language=spanish&tab=vocabulary',
   'Learn Spanish',
   '2025-08-01',
   2),
  ('4-Year Latin Learning Path',
   'Complete Latin curriculum based on the Henle textbooks, digitized into an interactive online learning format with exercises and assessments.',
   'AcademicCapIcon',
   '/learning-path/complete-henle-latin-program/overview',
   'Explore Latin Path',
   '2025-08-01',
   3);

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_news_items_updated_at BEFORE UPDATE ON news_items
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();