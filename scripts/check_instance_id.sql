-- Check instance_id configuration which might be causing Auth API issues
-- Run this in Supabase SQL Editor

-- 1. Check what instance_id values exist in the database
SELECT 
  'Current instance_ids in auth.users' as check,
  instance_id,
  COUNT(*) as user_count
FROM auth.users
GROUP BY instance_id;

-- 2. Check if there's a default instance_id configured
SELECT 
  'Auth schema config' as check,
  current_setting('app.settings.jwt_secret', true) as jwt_secret_exists,
  current_setting('request.jwt.claim.sub', true) as jwt_claim;

-- 3. Get the actual instance_id that should be used
SELECT 
  'Project instance_id' as check,
  id as instance_id
FROM auth.schema_migrations
LIMIT 1;

-- 4. Check for any auth hooks or functions that might be interfering
SELECT 
  n.nspname as schema_name,
  p.proname as function_name,
  pg_get_functiondef(p.oid) as function_definition
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'auth'
  AND p.proname LIKE '%before%'
  OR p.proname LIKE '%hook%'
  OR p.proname LIKE '%validate%';

-- 5. Check if auth.users has all required columns
SELECT 
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_schema = 'auth' 
  AND table_name = 'users'
ORDER BY ordinal_position;