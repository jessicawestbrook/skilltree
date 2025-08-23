-- Check Auth configuration and find the root cause
-- Run this in Supabase SQL Editor

-- ================================================
-- PART 1: Check auth schema tables
-- ================================================
SELECT 
  'Auth Tables' as category,
  table_name,
  'EXISTS' as status
FROM information_schema.tables 
WHERE table_schema = 'auth'
ORDER BY table_name;

-- ================================================
-- PART 2: Check for any constraints on auth.users
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
-- PART 3: Check for triggers on auth.users
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
  AND NOT t.tgisinternal
ORDER BY t.tgname;

-- ================================================
-- PART 4: Check auth.identities table
-- ================================================
SELECT COUNT(*) as total_identities
FROM auth.identities;

-- ================================================
-- PART 5: Check for any existing users
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
-- PART 6: Check instance_id values
-- ================================================
SELECT DISTINCT 
  instance_id, 
  COUNT(*) as user_count
FROM auth.users
GROUP BY instance_id;

-- ================================================
-- PART 7: Check for BEFORE INSERT triggers
-- ================================================
SELECT 
  t.tgname as trigger_name,
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
  AND (t.tgtype & 2 = 2)
  AND (t.tgtype & 4 = 4);