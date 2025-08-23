-- Remove NOT NULL constraints that are preventing word insertion
-- Generated on 2025-08-23T06:30:00.000Z

-- Remove NOT NULL constraints from columns that don't have data in PDF extraction
ALTER TABLE spelling_words ALTER COLUMN definition DROP NOT NULL;
ALTER TABLE spelling_words ALTER COLUMN example_sentence DROP NOT NULL;
ALTER TABLE spelling_words ALTER COLUMN pronunciation_guide DROP NOT NULL;
ALTER TABLE spelling_words ALTER COLUMN etymology DROP NOT NULL;

-- Verify the constraints were removed
SELECT 
    column_name,
    is_nullable,
    data_type
FROM information_schema.columns 
WHERE table_name = 'spelling_words' 
    AND column_name IN ('definition', 'example_sentence', 'pronunciation_guide', 'etymology')
ORDER BY column_name;