-- Update existing news items to August 2025
UPDATE news_items 
SET date_posted = '2025-08-01'
WHERE date_posted = '2024-12-01';

-- Verify the update
SELECT id, title, date_posted FROM news_items ORDER BY display_order;