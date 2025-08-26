-- Create tables for learning and review deck system
-- This allows cards to progress from learning → review based on mastery

-- First, add deck_status to track where each starred item is in the learning process
ALTER TABLE user_study_list_items
ADD COLUMN IF NOT EXISTS deck_status TEXT DEFAULT 'learning';

-- Add check constraint for valid deck statuses
ALTER TABLE user_study_list_items
DROP CONSTRAINT IF EXISTS user_study_list_items_deck_status_check;

ALTER TABLE user_study_list_items
ADD CONSTRAINT user_study_list_items_deck_status_check 
CHECK (deck_status IN ('learning', 'review', 'mastered'));

-- Add learning statistics columns
ALTER TABLE user_study_list_items
ADD COLUMN IF NOT EXISTS consecutive_correct INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS total_reviews INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_reviewed_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS promoted_to_review_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS mastered_at TIMESTAMPTZ;

-- Create index for efficient deck queries
CREATE INDEX IF NOT EXISTS idx_user_study_list_deck_status 
ON user_study_list_items(user_id, item_type, deck_status);

-- Add comments
COMMENT ON COLUMN user_study_list_items.deck_status IS 'Current deck status: learning (new/difficult), review (graduated), mastered (fully learned)';
COMMENT ON COLUMN user_study_list_items.consecutive_correct IS 'Number of consecutive correct answers';
COMMENT ON COLUMN user_study_list_items.total_reviews IS 'Total number of times this item has been reviewed';
COMMENT ON COLUMN user_study_list_items.promoted_to_review_at IS 'When the card graduated from learning to review';
COMMENT ON COLUMN user_study_list_items.mastered_at IS 'When the card was marked as fully mastered';

-- Create a view for easy access to language vocabulary deck items
CREATE OR REPLACE VIEW user_vocabulary_decks AS
SELECT 
  usli.*,
  lv.word,
  lv.pronunciation_guide,
  lv.english_translation,
  lv.definition_english,
  lv.part_of_speech,
  lv.difficulty_id,
  lv.vocabulary_type,
  lv.language,
  CASE 
    WHEN usli.deck_status = 'learning' THEN 1
    WHEN usli.deck_status = 'review' THEN 2
    WHEN usli.deck_status = 'mastered' THEN 3
  END as deck_priority
FROM user_study_list_items usli
JOIN language_vocabulary lv ON usli.item_id = lv.id::text
WHERE usli.item_type = 'language_vocabulary'
ORDER BY deck_priority, usli.added_at DESC;

-- Grant permissions
GRANT SELECT ON user_vocabulary_decks TO anon;
GRANT SELECT ON user_vocabulary_decks TO authenticated;