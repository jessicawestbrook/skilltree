-- Check existing table structures to see what columns they have
-- Run these queries one by one to see the current database schema

-- Check if user_progress table exists and what columns it has
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'user_progress' 
ORDER BY ordinal_position;

-- Check if starred_items table exists and what columns it has  
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'starred_items' 
ORDER BY ordinal_position;

-- Check what tables already exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('notifications', 'notification_preferences', 'user_progress', 'starred_items')
ORDER BY table_name;

-- Check all public tables to see what we have
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;