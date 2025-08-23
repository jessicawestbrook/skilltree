-- Create Jessica's user account directly in the database
-- Run this in Supabase SQL Editor

DO $$
DECLARE
  user_id UUID := gen_random_uuid();
  user_email TEXT := 'jessicawestbrook88@gmail.com';
  user_password TEXT := 'TestPassword123!';
BEGIN
  -- 1. Check if user already exists
  IF EXISTS (SELECT 1 FROM auth.users WHERE email = user_email) THEN
    RAISE NOTICE 'User already exists with email: %', user_email;
    
    -- Get the existing user ID
    SELECT id INTO user_id FROM auth.users WHERE email = user_email LIMIT 1;
    RAISE NOTICE 'Existing User ID: %', user_id;
  ELSE
    -- 2. Create new user in auth.users
    INSERT INTO auth.users (
      id,
      email,
      encrypted_password,
      email_confirmed_at,
      created_at,
      updated_at,
      raw_app_meta_data,
      raw_user_meta_data,
      is_super_admin,
      role,
      instance_id,
      aud,
      confirmation_token,
      recovery_token
    ) VALUES (
      user_id,
      user_email,
      crypt(user_password, gen_salt('bf')),
      NOW(), -- Mark as confirmed
      NOW(),
      NOW(),
      '{"provider": "email", "providers": ["email"]}',
      '{}',
      false,
      'authenticated',
      '00000000-0000-0000-0000-000000000000',
      'authenticated',
      '',
      ''
    );
    
    RAISE NOTICE '✅ User created successfully!';
    RAISE NOTICE 'User ID: %', user_id;
  END IF;
  
  -- 3. Create or update profile
  INSERT INTO public.profiles (
    id,
    email,
    created_at,
    updated_at
  ) VALUES (
    user_id,
    user_email,
    NOW(),
    NOW()
  )
  ON CONFLICT (id) DO UPDATE
  SET 
    email = EXCLUDED.email,
    updated_at = NOW();
  
  RAISE NOTICE '✅ Profile created/updated successfully!';
  
  -- 4. Create identity record
  INSERT INTO auth.identities (
    id,
    user_id,
    identity_data,
    provider,
    created_at,
    updated_at,
    provider_id,
    email,
    last_sign_in_at
  ) VALUES (
    user_id,
    user_id,
    jsonb_build_object(
      'sub', user_id::text,
      'email', user_email,
      'email_verified', true
    ),
    'email',
    NOW(),
    NOW(),
    user_id::text,
    user_email,
    NOW()
  )
  ON CONFLICT (provider, provider_id) DO UPDATE
  SET 
    email = EXCLUDED.email,
    updated_at = NOW();
  
  RAISE NOTICE '✅ Identity created/updated successfully!';
  
  RAISE NOTICE '';
  RAISE NOTICE '========================================';
  RAISE NOTICE '✅ USER SETUP COMPLETE!';
  RAISE NOTICE '========================================';
  RAISE NOTICE 'Email: %', user_email;
  RAISE NOTICE 'Password: %', user_password;
  RAISE NOTICE 'User ID: %', user_id;
  RAISE NOTICE '';
  RAISE NOTICE 'You can now log in at http://localhost:3000';
  RAISE NOTICE '========================================';
  
EXCEPTION
  WHEN OTHERS THEN
    RAISE NOTICE '❌ Error: %', SQLERRM;
    RAISE NOTICE 'SQLState: %', SQLSTATE;
END $$;