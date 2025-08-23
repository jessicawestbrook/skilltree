-- Check Auth configuration and constraints
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
  AND conrelid = 'auth.users'::regclass;

-- ================================================
-- STEP 3: Check for any rules or policies on auth.users
-- ================================================
SELECT 
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE schemaname = 'auth' AND tablename = 'users';

-- ================================================
-- STEP 4: Check auth.identities table
-- ================================================
SELECT COUNT(*) as identity_count
FROM auth.identities;

-- Check if there's an identity for Jessica
SELECT *
FROM auth.identities
WHERE email = 'jessicawestbrook88@gmail.com';

-- ================================================
-- STEP 5: Check auth configuration
-- ================================================
SELECT 
  key,
  value
FROM auth.config
WHERE key IN (
  'enable_signup',
  'enable_manual_linking', 
  'disable_signup',
  'email_auth_provider',
  'external_email_enabled'
);

-- ================================================
-- STEP 6: Check for any blocking functions
-- ================================================
SELECT 
  n.nspname as schema_name,
  p.proname as function_name,
  pg_get_function_result(p.oid) as return_type
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'auth'
  AND p.proname LIKE '%signup%'
   OR p.proname LIKE '%create%user%'
   OR p.proname LIKE '%before%'
   OR p.proname LIKE '%validate%';

-- ================================================
-- STEP 7: Check if email domain is blocked
-- ================================================
-- Some Supabase projects block certain email domains
SELECT *
FROM auth.blocked_email_domains
WHERE domain = 'gmail.com'
   OR domain = '@gmail.com';

-- ================================================
-- STEP 8: Check rate limiting
-- ================================================
-- Check if there's rate limiting on signups
SELECT *
FROM auth.rate_limits
WHERE action = 'signup'
   OR action = 'email_signup';

-- ================================================
-- RESULTS INTERPRETATION
-- ================================================
DO $$
BEGIN
  RAISE NOTICE '';
  RAISE NOTICE '========================================';
  RAISE NOTICE 'AUTH CONFIGURATION CHECK COMPLETE';
  RAISE NOTICE '========================================';
  RAISE NOTICE '';
  RAISE NOTICE 'Check the results above for:';
  RAISE NOTICE '1. Any disabled signup settings';
  RAISE NOTICE '2. Blocked email domains';
  RAISE NOTICE '3. Rate limiting issues';
  RAISE NOTICE '4. Custom validation functions blocking signup';
  RAISE NOTICE '';
  RAISE NOTICE 'The issue is likely in the Auth configuration,';
  RAISE NOTICE 'not in the trigger or profiles table.';
  RAISE NOTICE '========================================';
END $$;