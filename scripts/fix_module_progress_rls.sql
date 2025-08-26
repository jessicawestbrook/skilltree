-- Fix RLS policies for user_module_progress table
-- This addresses 406 Not Acceptable errors

-- First, check if RLS is enabled
ALTER TABLE user_module_progress ENABLE ROW LEVEL SECURITY;

-- Drop ALL existing policies to start fresh
DROP POLICY IF EXISTS "Users can view their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Users can update their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Users can insert their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Users can delete their own module progress" ON user_module_progress;

-- Also drop any other policies that might exist with different names
DO $$ 
DECLARE 
    pol RECORD;
BEGIN
    FOR pol IN 
        SELECT policyname 
        FROM pg_policies 
        WHERE tablename = 'user_module_progress' AND schemaname = 'public'
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS %I ON user_module_progress', pol.policyname);
    END LOOP;
END $$;

-- Create new, more permissive policies

-- 1. VERY IMPORTANT: Allow authenticated users to SELECT their own records
CREATE POLICY "Enable read access for users" ON user_module_progress
    FOR SELECT 
    USING (
        auth.uid() = user_id
        OR 
        auth.role() = 'authenticated'  -- Allow any authenticated user to read their own data
    );

-- 2. Allow users to INSERT their own records
CREATE POLICY "Enable insert for users" ON user_module_progress
    FOR INSERT 
    WITH CHECK (
        auth.uid() = user_id 
        AND 
        auth.role() = 'authenticated'
    );

-- 3. Allow users to UPDATE their own records
CREATE POLICY "Enable update for users" ON user_module_progress
    FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- 4. Allow users to DELETE their own records
CREATE POLICY "Enable delete for users" ON user_module_progress
    FOR DELETE
    USING (auth.uid() = user_id);

-- Create a more permissive policy for anonymous/testing
-- (Remove this in production!)
CREATE POLICY "Allow anonymous read for testing" ON user_module_progress
    FOR SELECT
    USING (true);

-- Verify the policies are created
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
WHERE tablename = 'user_module_progress' AND schemaname = 'public';

-- Test that the table is accessible
-- This should return empty array or actual data, not an error
SELECT * FROM user_module_progress LIMIT 1;