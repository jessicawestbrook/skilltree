const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function verifySpacedRepetitionTables() {
  try {
    console.log('Verifying spaced repetition tables...\n')
    
    // Check if user_flashcard_reviews table exists
    const { data: reviewsTable, error: reviewsError } = await supabase
      .from('user_flashcard_reviews')
      .select('*')
      .limit(1)
    
    if (reviewsError && reviewsError.code === '42P01') {
      console.log('❌ user_flashcard_reviews table does not exist')
      console.log('   Please run the migration script: supabase/migrations/20250823_create_spaced_repetition.sql')
    } else if (reviewsError) {
      console.log('⚠️  user_flashcard_reviews table exists but has an error:', reviewsError.message)
    } else {
      console.log('✅ user_flashcard_reviews table exists')
      
      // Get count of records
      const { count } = await supabase
        .from('user_flashcard_reviews')
        .select('*', { count: 'exact', head: true })
      
      console.log(`   Total review records: ${count || 0}`)
    }
    
    // Check if flashcard_review_history table exists
    const { data: historyTable, error: historyError } = await supabase
      .from('flashcard_review_history')
      .select('*')
      .limit(1)
    
    if (historyError && historyError.code === '42P01') {
      console.log('❌ flashcard_review_history table does not exist')
      console.log('   Please run the migration script: supabase/migrations/20250823_create_spaced_repetition.sql')
    } else if (historyError) {
      console.log('⚠️  flashcard_review_history table exists but has an error:', historyError.message)
    } else {
      console.log('✅ flashcard_review_history table exists')
      
      // Get count of records
      const { count } = await supabase
        .from('flashcard_review_history')
        .select('*', { count: 'exact', head: true })
      
      console.log(`   Total history records: ${count || 0}`)
    }
    
    console.log('\n📝 Migration Instructions:')
    console.log('If tables are missing, you need to run the SQL migration in Supabase:')
    console.log('1. Go to your Supabase dashboard')
    console.log('2. Navigate to SQL Editor')
    console.log('3. Copy and run the contents of: supabase/migrations/20250823_create_spaced_repetition.sql')
    console.log('\nThe migration file is located at:')
    console.log('C:\\Users\\jessi\\Projects\\skilltree2\\supabase\\migrations\\20250823_create_spaced_repetition.sql')
    
  } catch (error) {
    console.error('Fatal error:', error)
  }
}

// Run the verification
verifySpacedRepetitionTables()