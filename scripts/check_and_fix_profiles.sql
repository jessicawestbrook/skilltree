-- Check and fix profiles table structure
-- Run this in Supabase SQL Editor

-- 1. Check current structure of profiles table
SELECT 
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'profiles'
ORDER BY ordinal_position;

-- 2. Add username column if it doesn't exist
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS username TEXT UNIQUE;

-- 3. Verify the column was added
SELECT 
  'After adding username' as status,
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'profiles'
  AND column_name = 'username';

-- 4. Now create Jessica's user
DO $$
DECLARE
  user_id UUID;
  user_email TEXT := 'jessicawestbrook88@gmail.com';
  user_username TEXT := 'mangojess';  -- Your desired username
  user_password TEXT := 'TestPassword123!';
  correct_instance_id UUID;
BEGIN
  RAISE NOTICE 'Starting user creation process...';
  
  -- Get instance_id from existing users or use default
  SELECT DISTINCT instance_id INTO correct_instance_id 
  FROM auth.users 
  WHERE instance_id IS NOT NULL
  LIMIT 1;
  
  IF correct_instance_id IS NULL THEN
    correct_instance_id := '00000000-0000-0000-0000-000000000000';
  END IF;
  
  RAISE NOTICE 'Using instance_id: %', correct_instance_id;
  
  -- Check if user exists
  SELECT id INTO user_id FROM auth.users WHERE email = user_email;
  
  IF user_id IS NOT NULL THEN
    RAISE NOTICE 'User already exists with ID: %', user_id;
    
    -- Update password
    UPDATE auth.users 
    SET 
      encrypted_password = crypt(user_password, gen_salt('bf')),
      email_confirmed_at = NOW(),
      updated_at = NOW()
    WHERE id = user_id;
    
    RAISE NOTICE 'Updated password for existing user';
  ELSE
    -- Create new user
    user_id := gen_random_uuid();
    RAISE NOTICE 'Creating new user with ID: %', user_id;
    
    INSERT INTO auth.users (
      id,
      instance_id,
      aud,
      role,
      email,
      encrypted_password,
      email_confirmed_at,
      created_at,
      updated_at,
      raw_app_meta_data,
      raw_user_meta_data,
      is_super_admin
    ) VALUES (
      user_id,
      correct_instance_id,
      'authenticated',
      'authenticated',
      user_email,
      crypt(user_password, gen_salt('bf')),
      NOW(),
      NOW(),
      NOW(),
      '{"provider": "email", "providers": ["email"]}',
      '{}',
      false
    );
    
    RAISE NOTICE 'User created in auth.users';
  END IF;
  
  -- Create or update profile
  INSERT INTO public.profiles (
    id,
    email,
    username,
    created_at,
    updated_at
  ) VALUES (
    user_id,
    user_email,
    user_username,
    NOW(),
    NOW()
  )
  ON CONFLICT (id) DO UPDATE
  SET 
    email = EXCLUDED.email,
    username = COALESCE(public.profiles.username, EXCLUDED.username),
    updated_at = NOW();
  
  RAISE NOTICE 'Profile created/updated';
  
  -- Create identity
  INSERT INTO auth.identities (
    id,
    user_id,
    provider_id,
    provider,
    identity_data,
    created_at,
    updated_at
  ) VALUES (
    gen_random_uuid(),
    user_id,
    user_id::text,
    'email',
    jsonb_build_object(
      'sub', user_id::text,
      'email', user_email,
      'email_verified', true
    ),
    NOW(),
    NOW()
  )
  ON CONFLICT (provider, provider_id) DO UPDATE
  SET 
    identity_data = EXCLUDED.identity_data,
    updated_at = NOW();
  
  RAISE NOTICE 'Identity created/updated';
  
  RAISE NOTICE '';
  RAISE NOTICE '========================================';
  RAISE NOTICE '✅ USER SETUP COMPLETE!';
  RAISE NOTICE '========================================';
  RAISE NOTICE 'Email: %', user_email;
  RAISE NOTICE 'Username: %', user_username;
  RAISE NOTICE 'Password: %', user_password;
  RAISE NOTICE 'User ID: %', user_id;
  RAISE NOTICE '========================================';
  
EXCEPTION
  WHEN OTHERS THEN
    RAISE NOTICE '❌ ERROR: %', SQLERRM;
    RAISE NOTICE 'SQLState: %', SQLSTATE;
    RAISE;  -- Re-raise the error to see full details
END $$;

-- 5. Verify the user was created
SELECT 
  u.id,
  u.email,
  u.email_confirmed_at,
  u.created_at,
  p.username,
  p.email as profile_email
FROM auth.users u
LEFT JOIN public.profiles p ON u.id = p.id
WHERE u.email = 'jessicawestbrook88@gmail.com';