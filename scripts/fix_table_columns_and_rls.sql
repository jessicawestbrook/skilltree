-- Add missing columns to skill_tree_nodes if they don't exist
ALTER TABLE public.skill_tree_nodes 
ADD COLUMN IF NOT EXISTS type TEXT,
ADD COLUMN IF NOT EXISTS path TEXT,
ADD COLUMN IF NOT EXISTS learning_area TEXT;

-- Enable RLS on spelling_words table if not already enabled
ALTER TABLE public.spelling_words ENABLE ROW LEVEL SECURITY;

-- Drop existing policies on spelling_words if they exist
DROP POLICY IF EXISTS "Allow read access to all users" ON public.spelling_words;
DROP POLICY IF EXISTS "Enable read access for all users" ON public.spelling_words;

-- Create policy to allow all users to read spelling_words
CREATE POLICY "Enable read access for all users" 
  ON public.spelling_words 
  FOR SELECT 
  USING (true);

-- Grant permissions
GRANT SELECT ON public.spelling_words TO authenticated;
GRANT SELECT ON public.spelling_words TO anon;

-- Also ensure language_questions table has proper RLS
ALTER TABLE public.language_questions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Enable read access for all users" ON public.language_questions;

CREATE POLICY "Enable read access for all users" 
  ON public.language_questions 
  FOR SELECT 
  USING (true);

GRANT SELECT ON public.language_questions TO authenticated;
GRANT SELECT ON public.language_questions TO anon;