-- Standardized Tests System Schema
-- Supports IQ tests, SAT, ACT, LSAT, GRE, and other standardized assessments

-- Main standardized tests table
CREATE TABLE IF NOT EXISTS standardized_tests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    test_type VARCHAR(100) NOT NULL, -- 'iq', 'sat', 'act', 'lsat', 'gre', 'mcat', etc.
    subtype VARCHAR(100), -- 'ravens_matrices', 'stanford_binet', 'sat_math', 'sat_verbal', etc.
    description TEXT,
    total_questions INTEGER NOT NULL,
    time_limit_minutes INTEGER, -- Total test time limit
    scoring_method VARCHAR(100) NOT NULL, -- 'iq_scale', 'sat_scale', 'percentile', 'raw_score'
    max_score INTEGER,
    min_score INTEGER,
    passing_score INTEGER,
    source_url TEXT, -- Where the test content was sourced from
    version VARCHAR(50), -- Test version (e.g., "2024", "Form A", etc.)
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Standardized test questions table
CREATE TABLE IF NOT EXISTS standardized_test_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID NOT NULL REFERENCES standardized_tests(id) ON DELETE CASCADE,
    question_number INTEGER NOT NULL, -- Order within the test
    section VARCHAR(100), -- 'verbal', 'math', 'pattern_recognition', etc.
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL, -- 'multiple_choice', 'fill_in_blank', 'essay', etc.
    options JSONB, -- For multiple choice: ["option1", "option2", "option3", "option4"]
    correct_answer JSONB NOT NULL, -- For MC: index number, for others: correct answer(s)
    explanation TEXT,
    difficulty VARCHAR(20), -- 'easy', 'medium', 'hard', 'very_hard'
    points_value INTEGER DEFAULT 1, -- How many points this question is worth
    time_limit_seconds INTEGER, -- Individual question time limit
    image_url TEXT,
    audio_url TEXT,
    pattern_type VARCHAR(100), -- For IQ tests: 'arithmetic_progression', 'rotation', etc.
    cognitive_area VARCHAR(100), -- 'fluid_reasoning', 'working_memory', 'verbal_comprehension', etc.
    topic VARCHAR(100), -- 'algebra', 'geometry', 'reading_comprehension', etc.
    source_url TEXT,
    metadata JSONB, -- Additional flexible data storage
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(test_id, question_number)
);

-- User test attempts table
CREATE TABLE IF NOT EXISTS user_test_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL, -- References auth.users
    test_id UUID NOT NULL REFERENCES standardized_tests(id),
    attempt_number INTEGER NOT NULL DEFAULT 1,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    time_taken_seconds INTEGER,
    raw_score INTEGER,
    scaled_score INTEGER, -- IQ score, SAT score, etc.
    percentile REAL,
    section_scores JSONB, -- Breakdown by section/cognitive area
    is_completed BOOLEAN DEFAULT false,
    is_practice BOOLEAN DEFAULT false, -- true for practice tests
    metadata JSONB, -- Additional data like adaptive scoring info
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, test_id, attempt_number)
);

-- User question responses table
CREATE TABLE IF NOT EXISTS user_test_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID NOT NULL REFERENCES user_test_attempts(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES standardized_test_questions(id),
    user_answer JSONB, -- User's response
    is_correct BOOLEAN,
    points_earned INTEGER DEFAULT 0,
    time_taken_seconds INTEGER,
    response_metadata JSONB, -- Additional response data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(attempt_id, question_id)
);

-- Test sections/categories table (optional, for complex tests)
CREATE TABLE IF NOT EXISTS test_sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID NOT NULL REFERENCES standardized_tests(id) ON DELETE CASCADE,
    section_name VARCHAR(100) NOT NULL,
    section_order INTEGER NOT NULL,
    description TEXT,
    time_limit_minutes INTEGER,
    question_count INTEGER,
    scoring_weight REAL DEFAULT 1.0, -- How much this section counts toward total score
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(test_id, section_name),
    UNIQUE(test_id, section_order)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_standardized_tests_type ON standardized_tests(test_type);
CREATE INDEX IF NOT EXISTS idx_standardized_tests_subtype ON standardized_tests(test_type, subtype);
CREATE INDEX IF NOT EXISTS idx_test_questions_test_id ON standardized_test_questions(test_id);
CREATE INDEX IF NOT EXISTS idx_test_questions_section ON standardized_test_questions(test_id, section);
CREATE INDEX IF NOT EXISTS idx_test_questions_difficulty ON standardized_test_questions(difficulty);
CREATE INDEX IF NOT EXISTS idx_test_questions_pattern_type ON standardized_test_questions(pattern_type);
CREATE INDEX IF NOT EXISTS idx_user_attempts_user_test ON user_test_attempts(user_id, test_id);
CREATE INDEX IF NOT EXISTS idx_user_attempts_completed ON user_test_attempts(user_id, is_completed);
CREATE INDEX IF NOT EXISTS idx_user_responses_attempt ON user_test_responses(attempt_id);

-- Add some helpful comments
COMMENT ON TABLE standardized_tests IS 'Main table for standardized tests like IQ tests, SAT, ACT, etc.';
COMMENT ON TABLE standardized_test_questions IS 'Questions for standardized tests with rich metadata';
COMMENT ON TABLE user_test_attempts IS 'Tracks user attempts at standardized tests';
COMMENT ON TABLE user_test_responses IS 'Individual question responses within test attempts';
COMMENT ON TABLE test_sections IS 'Optional sections/categories within tests';

COMMENT ON COLUMN standardized_tests.scoring_method IS 'How scores are calculated: iq_scale (mean=100, sd=15), sat_scale (200-800), percentile, raw_score';
COMMENT ON COLUMN standardized_test_questions.pattern_type IS 'For IQ tests: type of cognitive pattern being tested';
COMMENT ON COLUMN standardized_test_questions.cognitive_area IS 'Cognitive domain: fluid_reasoning, crystallized_intelligence, working_memory, etc.';
COMMENT ON COLUMN user_test_attempts.scaled_score IS 'Final score in test-specific scale (IQ=100±15, SAT=200-800, etc.)';
COMMENT ON COLUMN user_test_responses.user_answer IS 'Flexible storage for any answer type: MC index, text, multiple selections, etc.';