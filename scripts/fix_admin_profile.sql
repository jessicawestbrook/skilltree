-- Fix admin profile for logged-in user
-- Run this in Supabase SQL Editor

-- The user ID from the error message
DO $$
DECLARE
  user_id UUID := '5876bd4e-5e68-4b4d-be15-8f0171bfae93';
  user_email TEXT;
BEGIN
  -- Get the user's email
  SELECT email INTO user_email 
  FROM auth.users 
  WHERE id = user_id;
  
  IF user_email IS NOT NULL THEN
    RAISE NOTICE 'Found user with email: %', user_email;
    
    -- Create or update the profile with admin privileges
    INSERT INTO public.profiles (
      id,
      email,
      is_admin,
      created_at,
      updated_at
    ) VALUES (
      user_id,
      user_email,
      true,  -- Set as admin
      NOW(),
      NOW()
    )
    ON CONFLICT (id) DO UPDATE
    SET 
      email = COALESCE(EXCLUDED.email, profiles.email),
      is_admin = true,  -- Ensure admin status
      updated_at = NOW();
    
    RAISE NOTICE '✅ Profile created/updated with admin privileges';
    
  ELSE
    RAISE NOTICE '❌ No user found with ID: %', user_id;
  END IF;
END $$;

-- Verify the profile was created
SELECT 
  id,
  email,
  username,
  is_admin,
  created_at,
  updated_at
FROM public.profiles
WHERE id = '5876bd4e-5e68-4b4d-be15-8f0171bfae93';

-- Also check all admin users
SELECT 
  'Admin Users' as category,
  COUNT(*) as count
FROM public.profiles
WHERE is_admin = true;

-- List all admin users
SELECT 
  id,
  email,
  username,
  is_admin
FROM public.profiles
WHERE is_admin = true;