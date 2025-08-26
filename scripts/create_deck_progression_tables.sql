-- Deck Progression System for Language Learning
-- Allows cards to move from learning -> review -> mastered based on performance

-- Create table for tracking vocabulary items in decks
CREATE TABLE IF NOT EXISTS user_vocabulary_decks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    vocabulary_id UUID NOT NULL,
    language VARCHAR(10) NOT NULL,
    deck_status VARCHAR(20) DEFAULT 'learning' CHECK (deck_status IN ('learning', 'review', 'mastered')),
    consecutive_correct INTEGER DEFAULT 0,
    total_reviews INTEGER DEFAULT 0,
    times_incorrect INTEGER DEFAULT 0,
    last_reviewed_at TIMESTAMPTZ,
    added_to_deck_at TIMESTAMPTZ DEFAULT NOW(),
    promoted_to_review_at TIMESTAMPTZ,
    mastered_at TIMESTAMPTZ,
    ease_factor NUMERIC(3,2) DEFAULT 2.5, -- For spaced repetition
    interval_days INTEGER DEFAULT 1,
    next_review_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, vocabulary_id)
);

-- Create table for tracking grammar questions in decks
CREATE TABLE IF NOT EXISTS user_grammar_decks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL,
    language_id UUID NOT NULL,
    deck_status VARCHAR(20) DEFAULT 'learning' CHECK (deck_status IN ('learning', 'review', 'mastered')),
    consecutive_correct INTEGER DEFAULT 0,
    total_reviews INTEGER DEFAULT 0,
    times_incorrect INTEGER DEFAULT 0,
    last_reviewed_at TIMESTAMPTZ,
    added_to_deck_at TIMESTAMPTZ DEFAULT NOW(),
    promoted_to_review_at TIMESTAMPTZ,
    mastered_at TIMESTAMPTZ,
    ease_factor NUMERIC(3,2) DEFAULT 2.5,
    interval_days INTEGER DEFAULT 1,
    next_review_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, question_id)
);

-- Create a unified view for all deck items
CREATE OR REPLACE VIEW user_deck_items AS
SELECT 
    'vocabulary' as item_type,
    id,
    user_id,
    vocabulary_id as item_id,
    language,
    deck_status,
    consecutive_correct,
    total_reviews,
    times_incorrect,
    last_reviewed_at,
    added_to_deck_at,
    promoted_to_review_at,
    mastered_at,
    ease_factor,
    interval_days,
    next_review_date
FROM user_vocabulary_decks
UNION ALL
SELECT 
    'grammar' as item_type,
    id,
    user_id,
    question_id as item_id,
    (SELECT code FROM languages WHERE id = language_id LIMIT 1) as language,
    deck_status,
    consecutive_correct,
    total_reviews,
    times_incorrect,
    last_reviewed_at,
    added_to_deck_at,
    promoted_to_review_at,
    mastered_at,
    ease_factor,
    interval_days,
    next_review_date
FROM user_grammar_decks;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_vocabulary_decks_user_status 
    ON user_vocabulary_decks(user_id, deck_status, language);
CREATE INDEX IF NOT EXISTS idx_user_vocabulary_decks_next_review 
    ON user_vocabulary_decks(user_id, next_review_date, deck_status);
CREATE INDEX IF NOT EXISTS idx_user_grammar_decks_user_status 
    ON user_grammar_decks(user_id, deck_status, language_id);
CREATE INDEX IF NOT EXISTS idx_user_grammar_decks_next_review 
    ON user_grammar_decks(user_id, next_review_date, deck_status);

-- Enable RLS
ALTER TABLE user_vocabulary_decks ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_grammar_decks ENABLE ROW LEVEL SECURITY;

-- RLS Policies for vocabulary decks
CREATE POLICY "Users can view own vocabulary deck items" ON user_vocabulary_decks
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own vocabulary deck items" ON user_vocabulary_decks
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own vocabulary deck items" ON user_vocabulary_decks
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own vocabulary deck items" ON user_vocabulary_decks
    FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for grammar decks
CREATE POLICY "Users can view own grammar deck items" ON user_grammar_decks
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own grammar deck items" ON user_grammar_decks
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own grammar deck items" ON user_grammar_decks
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own grammar deck items" ON user_grammar_decks
    FOR DELETE USING (auth.uid() = user_id);

-- Function to add item to learning deck when starred
CREATE OR REPLACE FUNCTION add_to_learning_deck()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if this is a vocabulary word being starred
    IF NEW.item_type = 'vocabulary_word' THEN
        INSERT INTO user_vocabulary_decks (
            user_id,
            vocabulary_id,
            language,
            deck_status,
            added_to_deck_at
        ) 
        SELECT 
            NEW.user_id,
            NEW.item_id::UUID,
            v.language,
            'learning',
            NOW()
        FROM language_vocabulary v
        WHERE v.id = NEW.item_id::UUID
        ON CONFLICT (user_id, vocabulary_id) DO NOTHING;
    
    -- Check if this is a grammar question being starred
    ELSIF NEW.item_type = 'language_question' THEN
        INSERT INTO user_grammar_decks (
            user_id,
            question_id,
            language_id,
            deck_status,
            added_to_deck_at
        )
        SELECT
            NEW.user_id,
            NEW.item_id::UUID,
            q.language_id,
            'learning',
            NOW()
        FROM language_questions q
        WHERE q.id = NEW.item_id::UUID
        ON CONFLICT (user_id, question_id) DO NOTHING;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically add to learning deck when starred
DROP TRIGGER IF EXISTS add_starred_to_learning_deck ON starred_items;
CREATE TRIGGER add_starred_to_learning_deck
    AFTER INSERT ON starred_items
    FOR EACH ROW
    EXECUTE FUNCTION add_to_learning_deck();

-- Function to calculate next review date based on spaced repetition
CREATE OR REPLACE FUNCTION calculate_next_review_date(
    p_ease_factor NUMERIC,
    p_interval_days INTEGER,
    p_difficulty VARCHAR
) RETURNS DATE AS $$
DECLARE
    v_new_interval INTEGER;
BEGIN
    IF p_difficulty = 'easy' THEN
        v_new_interval := GREATEST(CEIL(p_interval_days * p_ease_factor), 1);
    ELSIF p_difficulty = 'medium' THEN
        v_new_interval := GREATEST(CEIL(p_interval_days * 1.3), 1);
    ELSE -- hard
        v_new_interval := 1;
    END IF;
    
    RETURN CURRENT_DATE + v_new_interval;
END;
$$ LANGUAGE plpgsql;

-- Function to update deck status based on performance
CREATE OR REPLACE FUNCTION update_deck_progression()
RETURNS TRIGGER AS $$
BEGIN
    -- Update consecutive correct count
    IF NEW.last_reviewed_at IS NOT NULL THEN
        -- Promotion logic
        IF NEW.consecutive_correct >= 3 AND OLD.deck_status = 'learning' THEN
            NEW.deck_status := 'review';
            NEW.promoted_to_review_at := NOW();
        ELSIF NEW.consecutive_correct >= 5 AND OLD.deck_status = 'review' THEN
            NEW.deck_status := 'mastered';
            NEW.mastered_at := NOW();
        END IF;
        
        -- Demotion logic (if too many incorrect in a row)
        IF NEW.times_incorrect - OLD.times_incorrect >= 2 THEN
            IF OLD.deck_status = 'mastered' THEN
                NEW.deck_status := 'review';
                NEW.mastered_at := NULL;
                NEW.consecutive_correct := 0;
            ELSIF OLD.deck_status = 'review' THEN
                NEW.deck_status := 'learning';
                NEW.consecutive_correct := 0;
            END IF;
        END IF;
    END IF;
    
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for automatic progression
CREATE TRIGGER update_vocabulary_deck_progression
    BEFORE UPDATE ON user_vocabulary_decks
    FOR EACH ROW
    EXECUTE FUNCTION update_deck_progression();

CREATE TRIGGER update_grammar_deck_progression
    BEFORE UPDATE ON user_grammar_decks
    FOR EACH ROW
    EXECUTE FUNCTION update_deck_progression();

-- Add helper function to get deck statistics
CREATE OR REPLACE FUNCTION get_user_deck_stats(p_user_id UUID, p_language VARCHAR DEFAULT NULL)
RETURNS TABLE (
    deck_status VARCHAR,
    item_count BIGINT,
    due_today BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.deck_status,
        COUNT(*) as item_count,
        COUNT(CASE WHEN d.next_review_date <= CURRENT_DATE THEN 1 END) as due_today
    FROM user_deck_items d
    WHERE d.user_id = p_user_id
        AND (p_language IS NULL OR d.language = p_language)
    GROUP BY d.deck_status;
END;
$$ LANGUAGE plpgsql;