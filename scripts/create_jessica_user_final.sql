-- Final solution to create Jessica's user account
-- This uses the correct instance_id from existing users
-- Run this in Supabase SQL Editor

DO $$
DECLARE
  user_id UUID;
  user_email TEXT := 'jessicawestbrook88@gmail.com';
  user_password TEXT := 'TestPassword123!';
  correct_instance_id UUID;
BEGIN
  -- Get the correct instance_id from an existing user (if any)
  SELECT DISTINCT instance_id INTO correct_instance_id 
  FROM auth.users 
  WHERE instance_id IS NOT NULL
  LIMIT 1;
  
  -- If no users exist, use the default
  IF correct_instance_id IS NULL THEN
    correct_instance_id := '00000000-0000-0000-0000-000000000000';
  END IF;
  
  RAISE NOTICE 'Using instance_id: %', correct_instance_id;
  
  -- Check if user already exists
  SELECT id INTO user_id FROM auth.users WHERE email = user_email;
  
  IF user_id IS NOT NULL THEN
    -- User exists, update password
    UPDATE auth.users 
    SET 
      encrypted_password = crypt(user_password, gen_salt('bf')),
      updated_at = NOW(),
      email_confirmed_at = NOW()
    WHERE id = user_id;
    
    RAISE NOTICE '✅ Updated existing user password';
  ELSE
    -- Create new user
    user_id := gen_random_uuid();
    
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
      is_super_admin,
      confirmation_token,
      recovery_token,
      email_change_token_new,
      email_change
    ) VALUES (
      user_id,
      correct_instance_id,
      'authenticated',
      'authenticated', 
      user_email,
      crypt(user_password, gen_salt('bf')),
      NOW(), -- confirmed
      NOW(),
      NOW(),
      '{"provider": "email", "providers": ["email"]}',
      '{}',
      false,
      '', -- no confirmation needed
      '',
      NULL,
      NULL
    );
    
    RAISE NOTICE '✅ Created new user';
  END IF;
  
  -- Ensure profile exists
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
  
  RAISE NOTICE '✅ Profile created/updated';
  
  -- Ensure identity exists
  INSERT INTO auth.identities (
    id,
    user_id,
    provider_id,
    provider,
    identity_data,
    created_at,
    updated_at,
    email,
    last_sign_in_at
  ) VALUES (
    gen_random_uuid(),
    user_id,
    user_id::text,
    'email',
    jsonb_build_object(
      'sub', user_id::text,
      'email', user_email,
      'email_verified', true,
      'provider', 'email'
    ),
    NOW(),
    NOW(),
    user_email,
    NOW()
  )
  ON CONFLICT (provider, provider_id) DO UPDATE
  SET 
    identity_data = EXCLUDED.identity_data,
    email = EXCLUDED.email,
    updated_at = NOW();
  
  RAISE NOTICE '✅ Identity created/updated';
  
  RAISE NOTICE '';
  RAISE NOTICE '========================================';
  RAISE NOTICE '✅ SUCCESS! USER READY';
  RAISE NOTICE '========================================';
  RAISE NOTICE '';
  RAISE NOTICE 'Email: %', user_email;
  RAISE NOTICE 'Password: %', user_password;
  RAISE NOTICE 'User ID: %', user_id;
  RAISE NOTICE '';
  RAISE NOTICE 'You can now log in at http://localhost:3000';
  RAISE NOTICE '========================================';
  
EXCEPTION
  WHEN OTHERS THEN
    RAISE NOTICE '❌ Error occurred: %', SQLERRM;
    RAISE NOTICE 'SQLState: %', SQLSTATE;
    RAISE NOTICE 'Detail: Please check the error and try again';
END $$;

-- Verify the user was created
SELECT 
  'User Created' as status,
  id,
  email,
  email_confirmed_at,
  created_at
FROM auth.users
WHERE email = 'jessicawestbrook88@gmail.com';