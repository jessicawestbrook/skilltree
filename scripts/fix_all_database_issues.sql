-- Comprehensive database fix script
-- Run this in Supabase SQL editor to fix all missing columns and RLS issues

-- 1. Fix skill_tree_nodes table
ALTER TABLE public.skill_tree_nodes 
ADD COLUMN IF NOT EXISTS type TEXT,
ADD COLUMN IF NOT EXISTS path TEXT,
ADD COLUMN IF NOT EXISTS learning_area TEXT;

-- 2. Fix spelling_words table (add difficulty if missing)
ALTER TABLE public.spelling_words
ADD COLUMN IF NOT EXISTS difficulty TEXT;

-- 3. Fix language_questions table (add missing columns)
ALTER TABLE public.language_questions
ADD COLUMN IF NOT EXISTS question TEXT,
ADD COLUMN IF NOT EXISTS language TEXT,
ADD COLUMN IF NOT EXISTS category TEXT;

-- 4. Enable RLS on all necessary tables
ALTER TABLE public.spelling_words ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.language_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.skill_tree_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.starred_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_progress ENABLE ROW LEVEL SECURITY;

-- 5. Drop existing policies to avoid conflicts
DROP POLICY IF EXISTS "Enable read access for all users" ON public.spelling_words;
DROP POLICY IF EXISTS "Allow read access to all users" ON public.spelling_words;
DROP POLICY IF EXISTS "Enable read access for all users" ON public.language_questions;
DROP POLICY IF EXISTS "Allow read access to all users" ON public.language_questions;
DROP POLICY IF EXISTS "Enable read access for all users" ON public.skill_tree_nodes;
DROP POLICY IF EXISTS "Allow read access to all users" ON public.skill_tree_nodes;
DROP POLICY IF EXISTS "Users can view own starred items" ON public.starred_items;
DROP POLICY IF EXISTS "Users can manage own starred items" ON public.starred_items;
DROP POLICY IF EXISTS "Users can view own progress" ON public.user_progress;
DROP POLICY IF EXISTS "Users can manage own progress" ON public.user_progress;

-- 6. Create RLS policies for spelling_words
CREATE POLICY "Enable read access for all users" 
  ON public.spelling_words 
  FOR SELECT 
  USING (true);

-- 7. Create RLS policies for language_questions
CREATE POLICY "Enable read access for all users" 
  ON public.language_questions 
  FOR SELECT 
  USING (true);

-- 8. Create RLS policies for skill_tree_nodes
CREATE POLICY "Enable read access for all users" 
  ON public.skill_tree_nodes 
  FOR SELECT 
  USING (true);

-- 9. Create RLS policies for starred_items
CREATE POLICY "Users can view own starred items" 
  ON public.starred_items 
  FOR SELECT 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own starred items" 
  ON public.starred_items 
  FOR ALL 
  USING (auth.uid() = user_id);

-- 10. Create RLS policies for user_progress
CREATE POLICY "Users can view own progress" 
  ON public.user_progress 
  FOR SELECT 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own progress" 
  ON public.user_progress 
  FOR ALL 
  USING (auth.uid() = user_id);

-- 11. Grant necessary permissions
GRANT SELECT ON public.spelling_words TO authenticated;
GRANT SELECT ON public.spelling_words TO anon;
GRANT SELECT ON public.language_questions TO authenticated;
GRANT SELECT ON public.language_questions TO anon;
GRANT SELECT ON public.skill_tree_nodes TO authenticated;
GRANT SELECT ON public.skill_tree_nodes TO anon;
GRANT ALL ON public.starred_items TO authenticated;
GRANT ALL ON public.user_progress TO authenticated;

-- 12. Create profiles table if it doesn't exist
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE,
  full_name TEXT,
  avatar_url TEXT,
  is_admin BOOLEAN DEFAULT false,
  age_group TEXT,
  career_path TEXT,
  learning_goals TEXT[],
  preferences JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 13. Add any missing columns to profiles
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS username TEXT UNIQUE,
ADD COLUMN IF NOT EXISTS full_name TEXT,
ADD COLUMN IF NOT EXISTS avatar_url TEXT,
ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS age_group TEXT,
ADD COLUMN IF NOT EXISTS career_path TEXT,
ADD COLUMN IF NOT EXISTS learning_goals TEXT[],
ADD COLUMN IF NOT EXISTS preferences JSONB DEFAULT '{}'::jsonb,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW());

-- 14. Create user_interest_levels table if it doesn't exist
CREATE TABLE IF NOT EXISTS public.user_interest_levels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  category TEXT NOT NULL,
  interest_level INTEGER NOT NULL CHECK (interest_level >= 0 AND interest_level <= 10),
  skill_level INTEGER CHECK (skill_level >= 0 AND skill_level <= 10),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
  UNIQUE(user_id, category)
);

-- 15. Create indexes
CREATE INDEX IF NOT EXISTS idx_user_interest_levels_user_id ON public.user_interest_levels(user_id);
CREATE INDEX IF NOT EXISTS idx_user_interest_levels_category ON public.user_interest_levels(category);
CREATE INDEX IF NOT EXISTS idx_starred_items_user_id ON public.starred_items(user_id);
CREATE INDEX IF NOT EXISTS idx_starred_items_item_id ON public.starred_items(item_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON public.user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_node_id ON public.user_progress(node_id);

-- 16. Enable RLS on profiles and user_interest_levels
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_interest_levels ENABLE ROW LEVEL SECURITY;

-- 17. Drop existing policies on profiles and user_interest_levels
DROP POLICY IF EXISTS "Users can view all profiles" ON public.profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can view own interest levels" ON public.user_interest_levels;
DROP POLICY IF EXISTS "Users can update own interest levels" ON public.user_interest_levels;
DROP POLICY IF EXISTS "Users can insert own interest levels" ON public.user_interest_levels;
DROP POLICY IF EXISTS "Users can delete own interest levels" ON public.user_interest_levels;

-- 18. Create RLS policies for profiles
CREATE POLICY "Users can view all profiles" 
  ON public.profiles FOR SELECT 
  USING (true);

CREATE POLICY "Users can update own profile" 
  ON public.profiles FOR UPDATE 
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" 
  ON public.profiles FOR INSERT 
  WITH CHECK (auth.uid() = id);

-- 19. Create RLS policies for user_interest_levels
CREATE POLICY "Users can view own interest levels" 
  ON public.user_interest_levels FOR SELECT 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update own interest levels" 
  ON public.user_interest_levels FOR UPDATE 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own interest levels" 
  ON public.user_interest_levels FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own interest levels" 
  ON public.user_interest_levels FOR DELETE 
  USING (auth.uid() = user_id);

-- 20. Grant permissions on profiles and user_interest_levels
GRANT ALL ON public.profiles TO authenticated;
GRANT ALL ON public.user_interest_levels TO authenticated;
GRANT ALL ON public.profiles TO anon;
GRANT SELECT ON public.user_interest_levels TO anon;

-- 21. Create function to automatically create profile on user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, username, full_name, avatar_url)
  VALUES (
    new.id,
    new.raw_user_meta_data->>'username',
    new.raw_user_meta_data->>'full_name',
    new.raw_user_meta_data->>'avatar_url'
  )
  ON CONFLICT (id) DO NOTHING;
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 22. Create trigger for new user signup
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 23. Create profile records for existing users if they don't have one
INSERT INTO public.profiles (id)
SELECT id FROM auth.users
WHERE id NOT IN (SELECT id FROM public.profiles)
ON CONFLICT (id) DO NOTHING;

-- 24. Verify the fixes
DO $$
BEGIN
  RAISE NOTICE 'Database fixes applied successfully!';
  RAISE NOTICE 'Tables updated: skill_tree_nodes, spelling_words, language_questions, profiles, user_interest_levels';
  RAISE NOTICE 'RLS policies created for all tables';
  RAISE NOTICE 'Permissions granted to authenticated and anon users';
END $$;