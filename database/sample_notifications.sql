-- Sample Notifications Data
-- Run this AFTER creating the schema and AFTER you have logged in as a user
-- This will create sample notifications for testing

-- Replace 'YOUR_USER_ID' with your actual user ID from auth.users
-- You can get your user ID by running: SELECT id FROM auth.users WHERE email = 'your-email@example.com';

-- Sample achievement notification
INSERT INTO notifications (user_id, type, title, message, data) VALUES
('YOUR_USER_ID', 'achievement', 'Congratulations!', 'You completed your first skill tree module!', '{"category": "Mathematics", "skill": "Algebra Basics"}');

-- Sample progress notification  
INSERT INTO notifications (user_id, type, title, message, data) VALUES
('YOUR_USER_ID', 'progress', 'Learning Progress', 'You''re on a 3-day learning streak! Keep it up!', '{"streak_days": 3, "path": "/profile"}');

-- Sample reminder notification
INSERT INTO notifications (user_id, type, title, message, data) VALUES  
('YOUR_USER_ID', 'reminder', 'Time to Learn', 'You haven''t practiced spelling in 2 days. Ready for a quick session?', '{"path": "/spelling-bee"}');

-- Sample system notification
INSERT INTO notifications (user_id, type, title, message, data) VALUES
('YOUR_USER_ID', 'system', 'New Features Available', 'We''ve added new vocabulary training exercises! Check them out.', '{"path": "/vocabulary-trainer"}');

-- Sample social notification (if you have social features)
INSERT INTO notifications (user_id, type, title, message, data) VALUES
('YOUR_USER_ID', 'social', 'Challenge Completed', 'You''ve surpassed your friend''s score in the latest spelling bee challenge!', '{"friend_name": "Alex", "path": "/spelling-bee"}');

-- To check that the notifications were created:
-- SELECT * FROM notifications WHERE user_id = 'YOUR_USER_ID' ORDER BY created_at DESC;