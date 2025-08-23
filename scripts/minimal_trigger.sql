-- Minimal trigger that only uses ID
-- Run this in Supabase SQL Editor

-- ================================================
-- STEP 1: Remove old trigger/function
-- ================================================
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user() CASCADE;

-- ================================================
-- STEP 2: Create absolutely minimal trigger
-- ================================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  -- Do absolutely nothing except return NEW
  -- This tests if the trigger mechanism itself works
  RETURN NEW;
END;
$$;

-- Create trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- Grant permissions
GRANT EXECUTE ON FUNCTION public.handle_new_user() TO service_role;

-- ================================================
-- STEP 3: Verify
-- ================================================
SELECT 
  CASE 
    WHEN COUNT(*) > 0 THEN '✅ Minimal trigger created'
    ELSE '❌ Trigger not created'
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
  RAISE NOTICE '✅ MINIMAL TRIGGER CREATED';
  RAISE NOTICE '========================================';
  RAISE NOTICE '';
  RAISE NOTICE 'This trigger does NOTHING except return NEW.';
  RAISE NOTICE '';
  RAISE NOTICE 'Try signing up now.';
  RAISE NOTICE 'If it works, we can gradually add functionality.';
  RAISE NOTICE 'If it fails, the problem is not the trigger code.';
  RAISE NOTICE '========================================';
END $$;