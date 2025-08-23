-- Comprehensive fix for signup issues with jessicawestbrook88@gmail.com
-- Run this entire script in Supabase SQL Editor

-- ========================================
-- STEP 1: Check current state
-- ========================================
DO $$
BEGIN
  RAISE NOTICE 'Starting comprehensive signup fix...';
END $$;

-- Check if user exists in auth.users (for reference)
SELECT 
  'Auth Users Check' as check_type,
  COUNT(*) as count,
  STRING_AGG(email, ', ') as emails
FROM auth.users
WHERE email LIKE '%jessica%';

-- Check if profile exists
SELECT 
  'Profiles Check' as check_type,
  COUNT(*) as count,
  STRING_AGG(email, ', ') as emails
FROM profiles
WHERE email LIKE '%jessica%';

-- ========================================
-- STEP 2: Clean up any orphaned data
-- ========================================

-- Remove any orphaned profiles for this email
DELETE FROM profiles 
WHERE email = 'jessicawestbrook88@gmail.com'
  AND id NOT IN (SELECT id FROM auth.users);

-- ========================================
-- STEP 3: Drop existing trigger and function
-- ========================================
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user() CASCADE;

-- ========================================
-- STEP 4: Create improved trigger function
-- ========================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger 
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  profile_exists boolean;
BEGIN
  -- Check if profile already exists
  SELECT EXISTS(
    SELECT 1 FROM public.profiles WHERE id = NEW.id
  ) INTO profile_exists;
  
  IF profile_exists THEN
    -- Update existing profile
    UPDATE public.profiles
    SET 
      email = NEW.email,
      updated_at = NOW()
    WHERE id = NEW.id;
  ELSE
    -- Create new profile
    INSERT INTO public.profiles (
      id, 
      email, 
      username,
      created_at, 
      updated_at
    )
    VALUES (
      NEW.id,
      NEW.email,
      NULL, -- Username will be set later by user
      NOW(),
      NOW()
    );
  END IF;
  
  RETURN NEW;
EXCEPTION
  WHEN unique_violation THEN
    -- If there's a unique constraint violation on email, just update
    UPDATE public.profiles
    SET updated_at = NOW()
    WHERE id = NEW.id;
    RETURN NEW;
  WHEN OTHERS THEN
    -- Log error but don't block signup
    RAISE WARNING 'Profile creation error for user %: %', NEW.id, SQLERRM;
    RETURN NEW;
END;
$$;

-- ========================================
-- STEP 5: Create trigger
-- ========================================
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- ========================================
-- STEP 6: Fix permissions
-- ========================================
GRANT USAGE ON SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON public.profiles TO postgres, anon, authenticated, service_role;
GRANT EXECUTE ON FUNCTION public.handle_new_user() TO postgres, service_role;

-- ========================================
-- STEP 7: Fix RLS policies
-- ========================================
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Drop all existing policies
DROP POLICY IF EXISTS "Public profiles are viewable by everyone" ON profiles;
DROP POLICY IF EXISTS "Users can insert their own profile" ON profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
DROP POLICY IF EXISTS "Enable insert for authenticated users only" ON profiles;
DROP POLICY IF EXISTS "Enable update for users based on id" ON profiles;

-- Create comprehensive policies
CREATE POLICY "Anyone can view profiles"
  ON profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can insert their own profile"
  ON profiles FOR INSERT
  WITH CHECK (
    auth.uid() = id OR
    auth.role() = 'service_role'
  );

CREATE POLICY "Users can update their own profile"
  ON profiles FOR UPDATE
  USING (
    auth.uid() = id OR
    auth.role() = 'service_role'
  )
  WITH CHECK (
    auth.uid() = id OR
    auth.role() = 'service_role'
  );

-- ========================================
-- STEP 8: Ensure profiles table structure
-- ========================================
-- Add columns if they don't exist
DO $$
BEGIN
  -- Ensure email column exists and allows NULL
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'profiles' AND column_name = 'email'
  ) THEN
    ALTER TABLE profiles ADD COLUMN email TEXT;
  END IF;
  
  -- Make email nullable
  ALTER TABLE profiles ALTER COLUMN email DROP NOT NULL;
  
  -- Ensure username column exists
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'profiles' AND column_name = 'username'
  ) THEN
    ALTER TABLE profiles ADD COLUMN username TEXT UNIQUE;
  END IF;
  
  -- Ensure timestamps exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'profiles' AND column_name = 'created_at'
  ) THEN
    ALTER TABLE profiles ADD COLUMN created_at TIMESTAMPTZ DEFAULT NOW();
  END IF;
  
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'profiles' AND column_name = 'updated_at'
  ) THEN
    ALTER TABLE profiles ADD COLUMN updated_at TIMESTAMPTZ DEFAULT NOW();
  END IF;
END $$;

-- ========================================
-- STEP 9: Create unique constraint safely
-- ========================================
-- Drop existing constraint if it exists
ALTER TABLE profiles DROP CONSTRAINT IF EXISTS profiles_email_key;

-- Add unique constraint on email (allowing NULLs)
ALTER TABLE profiles 
ADD CONSTRAINT profiles_email_unique UNIQUE (email);

-- ========================================
-- STEP 10: Verify the fix
-- ========================================
SELECT 
  'Final Check - Triggers' as check_type,
  COUNT(*) as count
FROM pg_trigger t
JOIN pg_class c ON t.tgrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE n.nspname = 'auth' 
  AND c.relname = 'users'
  AND t.tgname = 'on_auth_user_created'

UNION ALL

SELECT 
  'Final Check - Policies' as check_type,
  COUNT(*) as count
FROM pg_policies
WHERE tablename = 'profiles'

UNION ALL

SELECT 
  'Final Check - Profiles' as check_type,
  COUNT(*) as count
FROM profiles
WHERE email = 'jessicawestbrook88@gmail.com';

-- ========================================
-- SUCCESS MESSAGE
-- ========================================
DO $$
BEGIN
  RAISE NOTICE '';
  RAISE NOTICE '✅ Signup fix completed successfully!';
  RAISE NOTICE '';
  RAISE NOTICE 'Next steps:';
  RAISE NOTICE '1. Try signing up with jessicawestbrook88@gmail.com';
  RAISE NOTICE '2. If signup succeeds, you should be able to log in';
  RAISE NOTICE '3. If it still fails, check the Auth Logs in Supabase dashboard';
END $$;