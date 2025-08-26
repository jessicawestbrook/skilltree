-- Computer Adaptive Learning (CAL) tables for language training

-- Table to store CAL sessions
CREATE TABLE IF NOT EXISTS language_cal_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    language_id UUID NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_updated TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_state JSONB DEFAULT '{}'::jsonb, -- Stores current state for resuming
    is_active BOOLEAN DEFAULT true,
    total_questions INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table to track performance by category
CREATE TABLE IF NOT EXISTS language_cal_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    language_id UUID NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'vocabulary', 'grammar', 'listening', 'reading'
    difficulty_level NUMERIC(3,2) DEFAULT 1.0, -- Current difficulty level (0.5 to 5.0)
    total_attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,
    last_attempt_at TIMESTAMPTZ,
    streak INTEGER DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, language_id, category)
);

-- Table to store individual question attempts in CAL sessions
CREATE TABLE IF NOT EXISTS language_cal_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES language_cal_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    language_id UUID NOT NULL,
    category VARCHAR(50) NOT NULL,
    question_id UUID NOT NULL,
    question_type VARCHAR(50),
    difficulty_level NUMERIC(3,2),
    is_correct BOOLEAN NOT NULL,
    response_time_ms INTEGER,
    answered_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_cal_sessions_user_language 
    ON language_cal_sessions(user_id, language_id, is_active);

CREATE INDEX IF NOT EXISTS idx_cal_performance_user_language 
    ON language_cal_performance(user_id, language_id);

CREATE INDEX IF NOT EXISTS idx_cal_attempts_session 
    ON language_cal_attempts(session_id, answered_at DESC);

CREATE INDEX IF NOT EXISTS idx_cal_attempts_user_category 
    ON language_cal_attempts(user_id, language_id, category, answered_at DESC);

-- Enable RLS
ALTER TABLE language_cal_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE language_cal_performance ENABLE ROW LEVEL SECURITY;
ALTER TABLE language_cal_attempts ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own CAL sessions" ON language_cal_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own CAL sessions" ON language_cal_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own CAL sessions" ON language_cal_sessions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own CAL performance" ON language_cal_performance
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own CAL performance" ON language_cal_performance
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own CAL performance" ON language_cal_performance
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own CAL attempts" ON language_cal_attempts
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own CAL attempts" ON language_cal_attempts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Function to update performance metrics after each attempt
CREATE OR REPLACE FUNCTION update_cal_performance()
RETURNS TRIGGER AS $$
BEGIN
    -- Update or insert performance record
    INSERT INTO language_cal_performance (
        user_id,
        language_id,
        category,
        total_attempts,
        correct_attempts,
        last_attempt_at,
        streak
    ) VALUES (
        NEW.user_id,
        NEW.language_id,
        NEW.category,
        1,
        CASE WHEN NEW.is_correct THEN 1 ELSE 0 END,
        NEW.answered_at,
        CASE WHEN NEW.is_correct THEN 1 ELSE 0 END
    )
    ON CONFLICT (user_id, language_id, category) 
    DO UPDATE SET
        total_attempts = language_cal_performance.total_attempts + 1,
        correct_attempts = language_cal_performance.correct_attempts + 
            CASE WHEN NEW.is_correct THEN 1 ELSE 0 END,
        last_attempt_at = NEW.answered_at,
        streak = CASE 
            WHEN NEW.is_correct THEN language_cal_performance.streak + 1
            ELSE 0
        END,
        -- Adjust difficulty based on performance
        difficulty_level = CASE
            -- If correct and streak >= 3, increase difficulty
            WHEN NEW.is_correct AND language_cal_performance.streak >= 2 
                THEN LEAST(language_cal_performance.difficulty_level + 0.1, 5.0)
            -- If incorrect, decrease difficulty
            WHEN NOT NEW.is_correct 
                THEN GREATEST(language_cal_performance.difficulty_level - 0.05, 0.5)
            -- Otherwise keep the same
            ELSE language_cal_performance.difficulty_level
        END,
        updated_at = NOW();
    
    -- Update session statistics
    UPDATE language_cal_sessions
    SET 
        total_questions = total_questions + 1,
        correct_answers = correct_answers + CASE WHEN NEW.is_correct THEN 1 ELSE 0 END,
        last_updated = NOW()
    WHERE id = NEW.session_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update performance
CREATE TRIGGER update_performance_on_attempt
    AFTER INSERT ON language_cal_attempts
    FOR EACH ROW
    EXECUTE FUNCTION update_cal_performance();