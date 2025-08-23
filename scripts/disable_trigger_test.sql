-- Temporarily disable trigger to test if it's the problem
-- Run this in Supabase SQL Editor

-- ================================================
-- OPTION 1: Completely remove the trigger
-- ================================================

-- Drop the trigger completely
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Drop the function
DROP FUNCTION IF EXISTS public.handle_new_user() CASCADE;

-- Check that it's gone
SELECT 
  CASE 
    WHEN COUNT(*) = 0 THEN '✅ Trigger removed successfully'
    ELSE '❌ Trigger still exists'
  END as status
FROM pg_trigger t
JOIN pg_class c ON t.tgrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE n.nspname = 'auth' 
  AND c.relname = 'users'
  AND t.tgname = 'on_auth_user_created';

-- ================================================
-- IMPORTANT
-- ================================================
DO $$
BEGIN
  RAISE NOTICE '';
  RAISE NOTICE '========================================';
  RAISE NOTICE '✅ TRIGGER REMOVED';
  RAISE NOTICE '========================================';
  RAISE NOTICE '';
  RAISE NOTICE 'The trigger has been completely removed.';
  RAISE NOTICE '';
  RAISE NOTICE 'Now try signing up with jessicawestbrook88@gmail.com';
  RAISE NOTICE '';
  RAISE NOTICE 'If signup works now, we know the trigger was the problem.';
  RAISE NOTICE 'You will need to manually create the profile after signup.';
  RAISE NOTICE '========================================';
END $$;