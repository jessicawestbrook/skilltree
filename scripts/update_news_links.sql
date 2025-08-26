-- Update news item links to be more specific
UPDATE news_items 
SET link = '/spelling-bee?tab=spelling'
WHERE title = 'Scripps Spelling Bee Study Lists Added';

UPDATE news_items 
SET link = '/language-trainer?language=spanish&tab=vocabulary'
WHERE title = '35,000 Spanish Vocabulary Words';

UPDATE news_items 
SET link = '/learning-path/complete-henle-latin-program/overview'
WHERE title = '4-Year Latin Learning Path';

-- Verify the updates
SELECT id, title, link FROM news_items ORDER BY display_order;