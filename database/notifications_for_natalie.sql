-- Sample Notifications for Natalie
-- Using the correct UUID from the error logs

-- Achievement notification
INSERT INTO notifications (user_id, type, title, message, data, is_read) VALUES
('2eaf6609-b02d-4d15-8b6d-197056945e31', 'achievement', '🏆 First Module Complete!', 'Congratulations! You completed your first skill tree module in Mathematics.', '{"category": "Mathematics", "skill": "Algebra Basics", "path": "/category/math"}', false);

-- Progress notification  
INSERT INTO notifications (user_id, type, title, message, data, is_read) VALUES
('2eaf6609-b02d-4d15-8b6d-197056945e31', 'progress', '🔥 3-Day Streak!', 'Amazing! You''re on a 3-day learning streak. Keep up the great work!', '{"streak_days": 3, "path": "/profile"}', false);

-- Reminder notification (unread)
INSERT INTO notifications (user_id, type, title, message, data, is_read) VALUES  
('2eaf6609-b02d-4d15-8b6d-197056945e31', 'reminder', '📚 Time for Spelling Practice', 'You haven''t practiced spelling in 2 days. Ready for a quick 5-minute session?', '{"last_practice": "2 days ago", "path": "/spelling-bee"}', false);

-- System notification (read)
INSERT INTO notifications (user_id, type, title, message, data, is_read) VALUES
('2eaf6609-b02d-4d15-8b6d-197056945e31', 'system', '✨ New Features Available', 'We''ve added new vocabulary training exercises and improved the user interface!', '{"features": ["vocabulary", "ui_improvements"], "path": "/vocabulary-trainer"}', true);

-- Social notification
INSERT INTO notifications (user_id, type, title, message, data, is_read) VALUES
('2eaf6609-b02d-4d15-8b6d-197056945e31', 'social', '🎯 Challenge Victory!', 'You''ve surpassed Alex''s score in the latest spelling bee challenge! Great job!', '{"challenger": "Alex", "your_score": 95, "their_score": 87, "path": "/spelling-bee"}', false);

-- Verify notifications were created
SELECT 
  id,
  type,
  title, 
  message,
  is_read,
  created_at
FROM notifications 
WHERE user_id = '2eaf6609-b02d-4d15-8b6d-197056945e31' 
ORDER BY created_at DESC;