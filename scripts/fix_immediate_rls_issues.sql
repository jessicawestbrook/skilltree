-- Quick fix for immediate RLS issues
-- Run this first to resolve 406 errors

-- 1. Disable RLS temporarily on problem tables to check if that's the issue
ALTER TABLE public.spelling_words DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.language_questions DISABLE ROW LEVEL SECURITY;

-- 2. Grant basic permissions
GRANT ALL ON public.spelling_words TO authenticated;
GRANT ALL ON public.spelling_words TO anon;
GRANT ALL ON public.spelling_words TO service_role;

GRANT ALL ON public.language_questions TO authenticated;
GRANT ALL ON public.language_questions TO anon;
GRANT ALL ON public.language_questions TO service_role;

-- 3. Verify the tables have the expected columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name = 'spelling_words'
ORDER BY ordinal_position;

-- 4. Check if there are any rows in spelling_words
SELECT COUNT(*) as total_rows FROM public.spelling_words;

-- 5. Test a simple query
SELECT id, word FROM public.spelling_words LIMIT 5;