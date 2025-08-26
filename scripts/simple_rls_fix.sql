-- Simple RLS fix for user_module_progress
-- This creates very permissive policies to ensure the table works

-- First, make sure RLS is enabled
ALTER TABLE user_module_progress ENABLE ROW LEVEL SECURITY;

-- Drop ALL existing policies
DROP POLICY IF EXISTS "Users can view their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Users can update their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Users can insert their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Users can delete their own module progress" ON user_module_progress;
DROP POLICY IF EXISTS "Enable read access for users" ON user_module_progress;
DROP POLICY IF EXISTS "Enable insert for users" ON user_module_progress;
DROP POLICY IF EXISTS "Enable update for users" ON user_module_progress;
DROP POLICY IF EXISTS "Enable delete for users" ON user_module_progress;
DROP POLICY IF EXISTS "Allow anonymous read for testing" ON user_module_progress;

-- Create a single, simple policy for all operations
-- This allows authenticated users to manage their own records
CREATE POLICY "Users manage own progress" ON user_module_progress
    FOR ALL 
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Verify the policy was created
SELECT 
    tablename,
    policyname,
    cmd
FROM pg_policies 
WHERE tablename = 'user_module_progress';