-- ================================================
-- ADD BIRTH YEAR FIELD TO USER PROFILES
-- ================================================
-- Adds birth_year field to user_profiles table for age calculation and content recommendations
-- ================================================

-- Add birth_year column to user_profiles table
ALTER TABLE public.user_profiles 
ADD COLUMN IF NOT EXISTS birth_year INTEGER CHECK (birth_year >= 1900 AND birth_year <= EXTRACT(YEAR FROM CURRENT_DATE));

-- Add index for birth year queries
CREATE INDEX IF NOT EXISTS idx_user_profiles_birth_year ON user_profiles(birth_year);

-- Create age groups view for content recommendations with calculated age
CREATE OR REPLACE VIEW age_groups AS
SELECT 
  id as user_id,
  birth_year,
  EXTRACT(YEAR FROM CURRENT_DATE) - birth_year as age,
  CASE 
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 5 AND 8 THEN 'early_elementary'
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 9 AND 11 THEN 'late_elementary'
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 12 AND 14 THEN 'middle_school'
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 15 AND 18 THEN 'high_school'
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 19 AND 22 THEN 'college'
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year >= 23 THEN 'adult'
    ELSE 'unspecified'
  END as age_group,
  CASE 
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 5 AND 8 THEN 1
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 9 AND 11 THEN 2
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 12 AND 14 THEN 3
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 15 AND 18 THEN 4
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year BETWEEN 19 AND 22 THEN 5
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - birth_year >= 23 THEN 6
    ELSE 0
  END as difficulty_level
FROM user_profiles
WHERE birth_year IS NOT NULL;

-- Grant permissions
GRANT SELECT ON age_groups TO authenticated;

-- ================================================
-- Verification
-- ================================================

DO $$
BEGIN
  RAISE NOTICE 'Age field added to user_profiles successfully!';
  RAISE NOTICE 'Age groups view created for content recommendations';
END $$;