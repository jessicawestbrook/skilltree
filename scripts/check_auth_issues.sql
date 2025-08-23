-- Check Auth configuration and find the root cause
-- Run this in Supabase SQL Editor

-- ================================================
-- STEP 1: Check auth schema tables
-- ================================================
SELECT 
  'Auth Tables' as category,
  table_name,
  'EXISTS' as status
FROM information_schema.tables 
WHERE table_schema = 'auth'
ORDER BY table_name;

-- ================================================
-- STEP 2: Check for any constraints on auth.users
-- ================================================
SELECT 
  conname as constraint_name,
  contype as constraint_type,
  pg_get_constraintdef(oid) as definition
FROM pg_constraint
WHERE connamespace = 'auth'::regnamespace
  AND conrelid = 'auth.users'::regclass
ORDER BY conname;

-- ================================================
-- STEP 3: Check for triggers on auth.users
-- ================================================
SELECT 
  t.tgname as trigger_name,
  CASE t.tgenabled 
    WHEN 'O' THEN 'ENABLED'
    WHEN 'D' THEN 'DISABLED'
    WHEN 'R' THEN 'REPLICA'
    WHEN 'A' THEN 'ALWAYS'
  END as status,
  p.proname as function_name
FROM pg_trigger t
JOIN pg_class c ON t.tgrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
LEFT JOIN pg_proc p ON t.tgfoid = p.oid
WHERE n.nspname = 'auth' 
  AND c.relname = 'users'
  AND NOT t.tgisinternal  -- Exclude system triggers
ORDER BY t.tgname;

-- ================================================
-- STEP 4: Check auth.identities table
-- ================================================
SELECT COUNT(*) as total_identities
FROM auth.identities;

-- ================================================
-- STEP 5: Check for any existing users
-- ================================================
SELECT COUNT(*) as total_users
FROM auth.users;

-- Show last 5 users created
SELECT 
  id,
  email,
  created_at,
  confirmed_at
FROM auth.users
ORDER BY created_at DESC
LIMIT 5;

-- ================================================
-- STEP 6: Check if there are any BEFORE INSERT triggers
-- ================================================
SELECT 
  t.tgname as trigger_name,
  t.tgtype as trigger_type,
  CASE 
    WHEN t.tgtype & 2 = 2 THEN 'BEFORE'
    WHEN t.tgtype & 64 = 64 THEN 'INSTEAD OF'
    ELSE 'AFTER'
  END as timing,
  CASE 
    WHEN t.tgtype & 4 = 4 THEN 'INSERT'
    WHEN t.tgtype & 8 = 8 THEN 'DELETE'
    WHEN t.tgtype & 16 = 16 THEN 'UPDATE'
  END as event,
  p.proname as function_name
FROM pg_trigger t
JOIN pg_class c ON t.tgrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
LEFT JOIN pg_proc p ON t.tgfoid = p.oid
WHERE n.nspname = 'auth' 
  AND c.relname = 'users'
  AND (t.tgtype & 2 = 2)  -- BEFORE triggers
  AND (t.tgtype & 4 = 4); -- INSERT triggers

-- ================================================
-- STEP 7: Check for custom functions that might block
-- ================================================
SELECT 
  n.nspname as schema_name,
  p.proname as function_name
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE p.proname IN (
  'before_insert_auth_users',
  'validate_user_signup',
  'check_user_signup',
  'on_auth_user_created'
);

-- ================================================
-- STEP 8: Test if we can insert directly into auth.users
-- ================================================
DO $$
DECLARE
  test_id UUID := gen_random_uuid();
BEGIN
  -- Try to insert a test user directly
  BEGIN
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
      'test_direct_' || extract(epoch from now()) || '@example.com',
      crypt('TestPassword123!', gen_salt('bf')),
      NOW(),
      NOW(),
      NOW(),
      '00000000-0000-0000-0000-000000000000'
    );
    
    -- If we get here, insert worked - delete the test user
    DELETE FROM auth.users WHERE id = test_id;
    RAISE NOTICE '✅ Direct insert into auth.users WORKS';
    
  EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE '❌ Direct insert FAILED: %', SQLERRM;
    RAISE NOTICE 'Error detail: %', SQLSTATE;
  END;
END $$;

-- ================================================
-- STEP 9: Check Supabase project settings
-- ================================================
-- Note: These settings are usually in the dashboard, not the database
-- But we can check for common issues

-- Check if instance_id is properly set
SELECT DISTINCT instance_id, COUNT(*) as user_count
FROM auth.users
GROUP BY instance_id;

-- ================================================
-- RESULTS
-- ================================================
DO $$
BEGIN
  RAISE NOTICE '';
  RAISE NOTICE '========================================';
  RAISE NOTICE 'CHECK THE RESULTS ABOVE FOR:';
  RAISE NOTICE '========================================';
  RAISE NOTICE '1. Any BEFORE INSERT triggers that might block';
  RAISE NOTICE '2. The direct insert test result';
  RAISE NOTICE '3. Total number of users (if 0, auth might be broken)';
  RAISE NOTICE '4. Any unusual constraints';
  RAISE NOTICE '';
  RAISE NOTICE 'If direct insert fails, the error message will';
  RAISE NOTICE 'tell us exactly what is blocking signup.';
  RAISE NOTICE '========================================';
END $$;