-- Add is_admin column to profiles table
-- This allows users to be granted admin privileges

-- First, create a backup of the profiles table
CREATE TABLE IF NOT EXISTS profiles_bkp AS SELECT * FROM profiles;

-- Add is_admin column to profiles table
ALTER TABLE profiles 
ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;

-- Add a comment to document the column purpose
COMMENT ON COLUMN profiles.is_admin IS 'Grants admin access to dashboard and management features';

-- Verify the column was added
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'profiles' 
  AND column_name = 'is_admin';

-- Show current structure
\d profiles;