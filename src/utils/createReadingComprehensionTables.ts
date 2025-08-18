import { supabase } from '../services/supabase'

export async function createReadingComprehensionTables() {
  try {
    // Create tables via SQL
    const { error: createTableError } = await supabase.rpc('exec_sql', {
      sql: `
        CREATE TABLE IF NOT EXISTS reading_passages (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          title VARCHAR(255) NOT NULL,
          passage_text TEXT NOT NULL,
          difficulty_level INTEGER NOT NULL CHECK (difficulty_level BETWEEN 1 AND 5),
          category VARCHAR(100),
          word_count INTEGER,
          source_url TEXT,
          source_attribution TEXT,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS comprehension_questions (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          passage_id UUID NOT NULL REFERENCES reading_passages(id) ON DELETE CASCADE,
          question_text TEXT NOT NULL,
          options JSONB NOT NULL,
          correct_answer_index INTEGER NOT NULL,
          explanation TEXT NOT NULL,
          question_type VARCHAR(50) CHECK (question_type IN ('main_idea', 'detail', 'inference', 'vocabulary', 'author_purpose')),
          order_index INTEGER NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS reading_comprehension_attempts (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
          passage_id UUID REFERENCES reading_passages(id) ON DELETE CASCADE,
          question_id UUID REFERENCES comprehension_questions(id) ON DELETE CASCADE,
          selected_answer INTEGER NOT NULL,
          is_correct BOOLEAN NOT NULL,
          time_taken INTEGER,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_reading_passages_difficulty ON reading_passages(difficulty_level);
        CREATE INDEX IF NOT EXISTS idx_reading_passages_category ON reading_passages(category);
        CREATE INDEX IF NOT EXISTS idx_comprehension_questions_passage ON comprehension_questions(passage_id);
        CREATE INDEX IF NOT EXISTS idx_comprehension_questions_type ON comprehension_questions(question_type);
        CREATE INDEX IF NOT EXISTS idx_reading_attempts_user ON reading_comprehension_attempts(user_id);
        CREATE INDEX IF NOT EXISTS idx_reading_attempts_passage ON reading_comprehension_attempts(passage_id);
      `
    })

    if (createTableError) {
      console.error('Error creating reading comprehension tables:', createTableError)
      return false
    }

    console.log('Reading comprehension tables created successfully!')
    return true
  } catch (error) {
    console.error('Error setting up reading comprehension:', error)
    return false
  }
}

export async function checkReadingComprehensionTables() {
  try {
    const { error } = await supabase
      .from('reading_passages')
      .select('count')
      .limit(1)

    if (error) {
      console.log('Reading passages table does not exist')
      return false
    }

    return true
  } catch (error) {
    return false
  }
}