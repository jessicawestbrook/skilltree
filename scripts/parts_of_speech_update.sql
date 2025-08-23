-- SQL script to update parts of speech in spelling_words table
-- Generated from NLP analysis using compromise library
-- Total updates: 4628 words

-- First, check if there's a problematic trigger
-- You may need to temporarily disable triggers if they reference non-existent columns

-- Sample updates (first 100 words)
UPDATE spelling_words SET part_of_speech = 'verb' WHERE id = 'b45f74f4-a268-40af-af15-9d7aa93ae47c'; -- sound
UPDATE spelling_words SET part_of_speech = 'verb' WHERE id = '005c6694-875c-4c22-aa04-76c56ca36373'; -- help
UPDATE spelling_words SET part_of_speech = 'noun' WHERE id = '00a7351a-ad32-4011-af5b-9da8fac7a391'; -- mystery
UPDATE spelling_words SET part_of_speech = 'noun' WHERE id = '00b13e64-6f5d-45ea-bd69-624ef4ac2cd5'; -- overrun
UPDATE spelling_words SET part_of_speech = 'adjective' WHERE id = '00c88760-4c75-4083-a29c-e40c455f0021'; -- spiteful

-- To generate the full update script, run:
-- node scripts/generate_sql_updates.js