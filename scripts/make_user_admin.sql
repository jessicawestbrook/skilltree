-- SQL script to make a user an admin
-- Run this in Supabase SQL Editor

-- Replace 'your-email@example.com' with the actual email of the user you want to make admin
UPDATE profiles
SET is_admin = true
WHERE email = 'your-email@example.com';

-- Verify the update
SELECT id, email, is_admin
FROM profiles
WHERE email = 'your-email@example.com';

-- To see all admin users
SELECT id, email, is_admin
FROM profiles
WHERE is_admin = true;