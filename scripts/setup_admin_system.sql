-- Setup admin system for SkillTree application
-- This script adds the necessary columns and creates helper functions

-- Step 1: Create backup of profiles table
CREATE TABLE IF NOT EXISTS profiles_bkp AS SELECT * FROM profiles;

-- Step 2: Add is_admin column to profiles table
ALTER TABLE profiles 
ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE;

-- Step 3: Add email column to profiles for easier admin management
ALTER TABLE profiles 
ADD COLUMN IF NOT EXISTS email TEXT;

-- Step 4: Create a function to sync email from auth.users to profiles
CREATE OR REPLACE FUNCTION sync_user_email()
RETURNS TRIGGER AS $$
BEGIN
    -- Update the profiles table with email from auth.users
    UPDATE profiles 
    SET email = NEW.email, updated_at = NOW()
    WHERE id = NEW.id;
    
    -- If profile doesn't exist, create it
    IF NOT FOUND THEN
        INSERT INTO profiles (id, email, created_at, updated_at)
        VALUES (NEW.id, NEW.email, NOW(), NOW())
        ON CONFLICT (id) DO UPDATE SET 
            email = NEW.email,
            updated_at = NOW();
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Step 5: Create trigger to auto-sync emails
DROP TRIGGER IF EXISTS sync_email_trigger ON auth.users;
CREATE TRIGGER sync_email_trigger
    AFTER INSERT OR UPDATE OF email ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION sync_user_email();

-- Step 6: Update existing profiles with emails from auth.users
UPDATE profiles 
SET email = auth.users.email, updated_at = NOW()
FROM auth.users 
WHERE profiles.id = auth.users.id 
  AND profiles.email IS NULL;

-- Step 7: Create a helper function to make a user admin by email
CREATE OR REPLACE FUNCTION make_user_admin(user_email TEXT)
RETURNS TABLE(user_id UUID, email TEXT, is_admin BOOLEAN) AS $$
BEGIN
    UPDATE profiles 
    SET is_admin = TRUE, updated_at = NOW()
    WHERE profiles.email = user_email;
    
    RETURN QUERY
    SELECT profiles.id, profiles.email, profiles.is_admin
    FROM profiles
    WHERE profiles.email = user_email;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Step 8: Show current admin users
SELECT id, email, is_admin, created_at 
FROM profiles 
WHERE is_admin = TRUE 
ORDER BY created_at;

-- Instructions for making a user admin:
-- SELECT * FROM make_user_admin('your-email@example.com');