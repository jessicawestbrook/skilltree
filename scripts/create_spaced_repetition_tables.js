const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function createSpacedRepetitionTables() {
  try {
    console.log('Creating spaced repetition tables...')
    
    // Create user_flashcard_reviews table
    const createReviewsTable = `
      CREATE TABLE IF NOT EXISTS user_flashcard_reviews (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
        flashcard_id TEXT NOT NULL,
        flashcard_type TEXT NOT NULL CHECK (flashcard_type IN ('vocabulary', 'spelling', 'language', 'question', 'skill_node')),
        last_reviewed TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        next_review TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        review_count INTEGER NOT NULL DEFAULT 0,
        easiness_factor DECIMAL(3,2) NOT NULL DEFAULT 2.5 CHECK (easiness_factor >= 1.3 AND easiness_factor <= 2.5),
        interval_days INTEGER NOT NULL DEFAULT 0,
        consecutive_correct INTEGER NOT NULL DEFAULT 0,
        total_correct INTEGER NOT NULL DEFAULT 0,
        total_attempts INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        UNIQUE(user_id, flashcard_id, flashcard_type)
      );
    `
    
    const { error: reviewsTableError } = await supabase.rpc('exec_sql', {
      sql: createReviewsTable
    })
    
    if (reviewsTableError) {
      console.error('Error creating user_flashcard_reviews table:', reviewsTableError)
    } else {
      console.log('✓ Created user_flashcard_reviews table')
    }
    
    // Create flashcard_review_history table for analytics
    const createHistoryTable = `
      CREATE TABLE IF NOT EXISTS flashcard_review_history (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
        flashcard_id TEXT NOT NULL,
        flashcard_type TEXT NOT NULL CHECK (flashcard_type IN ('vocabulary', 'spelling', 'language', 'question', 'skill_node')),
        quality_rating INTEGER NOT NULL CHECK (quality_rating >= 0 AND quality_rating <= 5),
        time_taken_seconds INTEGER,
        hint_used BOOLEAN DEFAULT FALSE,
        next_interval_days INTEGER,
        reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      );
    `
    
    const { error: historyTableError } = await supabase.rpc('exec_sql', {
      sql: createHistoryTable
    })
    
    if (historyTableError) {
      console.error('Error creating flashcard_review_history table:', historyTableError)
    } else {
      console.log('✓ Created flashcard_review_history table')
    }
    
    // Create indexes for performance
    const createIndexes = `
      CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_user_id ON user_flashcard_reviews(user_id);
      CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_next_review ON user_flashcard_reviews(next_review);
      CREATE INDEX IF NOT EXISTS idx_user_flashcard_reviews_type ON user_flashcard_reviews(flashcard_type);
      CREATE INDEX IF NOT EXISTS idx_flashcard_review_history_user_id ON flashcard_review_history(user_id);
      CREATE INDEX IF NOT EXISTS idx_flashcard_review_history_reviewed_at ON flashcard_review_history(reviewed_at);
    `
    
    const { error: indexError } = await supabase.rpc('exec_sql', {
      sql: createIndexes
    })
    
    if (indexError) {
      console.error('Error creating indexes:', indexError)
    } else {
      console.log('✓ Created indexes for performance')
    }
    
    // Create updated_at trigger
    const createTrigger = `
      CREATE OR REPLACE FUNCTION update_updated_at_column()
      RETURNS TRIGGER AS $$
      BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
      END;
      $$ language 'plpgsql';
      
      DROP TRIGGER IF EXISTS update_user_flashcard_reviews_updated_at ON user_flashcard_reviews;
      
      CREATE TRIGGER update_user_flashcard_reviews_updated_at
      BEFORE UPDATE ON user_flashcard_reviews
      FOR EACH ROW
      EXECUTE FUNCTION update_updated_at_column();
    `
    
    const { error: triggerError } = await supabase.rpc('exec_sql', {
      sql: createTrigger
    })
    
    if (triggerError) {
      console.error('Error creating trigger:', triggerError)
    } else {
      console.log('✓ Created updated_at trigger')
    }
    
    // Enable RLS
    const enableRLS = `
      ALTER TABLE user_flashcard_reviews ENABLE ROW LEVEL SECURITY;
      ALTER TABLE flashcard_review_history ENABLE ROW LEVEL SECURITY;
      
      -- Policies for user_flashcard_reviews
      DROP POLICY IF EXISTS "Users can view own flashcard reviews" ON user_flashcard_reviews;
      CREATE POLICY "Users can view own flashcard reviews" ON user_flashcard_reviews
        FOR SELECT USING (auth.uid() = user_id);
      
      DROP POLICY IF EXISTS "Users can insert own flashcard reviews" ON user_flashcard_reviews;
      CREATE POLICY "Users can insert own flashcard reviews" ON user_flashcard_reviews
        FOR INSERT WITH CHECK (auth.uid() = user_id);
      
      DROP POLICY IF EXISTS "Users can update own flashcard reviews" ON user_flashcard_reviews;
      CREATE POLICY "Users can update own flashcard reviews" ON user_flashcard_reviews
        FOR UPDATE USING (auth.uid() = user_id);
      
      DROP POLICY IF EXISTS "Users can delete own flashcard reviews" ON user_flashcard_reviews;
      CREATE POLICY "Users can delete own flashcard reviews" ON user_flashcard_reviews
        FOR DELETE USING (auth.uid() = user_id);
      
      -- Policies for flashcard_review_history
      DROP POLICY IF EXISTS "Users can view own review history" ON flashcard_review_history;
      CREATE POLICY "Users can view own review history" ON flashcard_review_history
        FOR SELECT USING (auth.uid() = user_id);
      
      DROP POLICY IF EXISTS "Users can insert own review history" ON flashcard_review_history;
      CREATE POLICY "Users can insert own review history" ON flashcard_review_history
        FOR INSERT WITH CHECK (auth.uid() = user_id);
    `
    
    const { error: rlsError } = await supabase.rpc('exec_sql', {
      sql: enableRLS
    })
    
    if (rlsError) {
      console.error('Error enabling RLS:', rlsError)
    } else {
      console.log('✓ Enabled Row Level Security with policies')
    }
    
    console.log('\n✅ Spaced repetition tables created successfully!')
    console.log('\nTables created:')
    console.log('  - user_flashcard_reviews: Tracks review scheduling and performance')
    console.log('  - flashcard_review_history: Stores review history for analytics')
    
  } catch (error) {
    console.error('Fatal error:', error)
  }
}

// Run the script
createSpacedRepetitionTables()