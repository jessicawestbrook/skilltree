-- Test direct insert into auth.users
-- Run this SEPARATELY in Supabase SQL Editor

DO $$
DECLARE
  test_id UUID := gen_random_uuid();
  test_email TEXT := 'test_' || extract(epoch from now())::text || '@example.com';
BEGIN
  -- Try to insert a test user directly
  BEGIN
    RAISE NOTICE 'Attempting to insert test user with email: %', test_email;
    
    INSERT INTO auth.users (
      id,
      email,
      encrypted_password,
      email_confirmed_at,
      created_at,
      updated_at,
      instance_id
    ) VALUES (
      test_id,
      test_email,
      crypt('TestPassword123!', gen_salt('bf')),
      NOW(),
      NOW(),
      NOW(),
      '00000000-0000-0000-0000-000000000000'
    );
    
    -- If we get here, insert worked
    RAISE NOTICE '✅ SUCCESS: Direct insert into auth.users WORKS!';
    
    -- Clean up the test user
    DELETE FROM auth.users WHERE id = test_id;
    RAISE NOTICE '✅ Test user cleaned up';
    
  EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE '❌ FAILED: Direct insert failed';
    RAISE NOTICE 'Error: %', SQLERRM;
    RAISE NOTICE 'SQLState: %', SQLSTATE;
    RAISE NOTICE '';
    RAISE NOTICE 'This error is preventing user signups!';
  END;
END $$;