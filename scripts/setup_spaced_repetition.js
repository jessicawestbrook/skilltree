const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkAndCreateTables() {
  console.log('Checking for spaced repetition tables...');
  
  // Check if user_flashcard_reviews table exists
  const { data: reviewsTable, error: reviewsError } = await supabase
    .from('user_flashcard_reviews')
    .select('id')
    .limit(1);
  
  if (reviewsError && reviewsError.code === '42P01') {
    console.log('❌ user_flashcard_reviews table does not exist');
    console.log('Please run the following SQL in your Supabase dashboard:');
    console.log('----------------------------------------');
    console.log('File: scripts/create_spaced_repetition_tables.sql');
    console.log('----------------------------------------');
  } else if (reviewsError && reviewsError.code === '42501') {
    console.log('⚠️  user_flashcard_reviews table exists but RLS policies may need adjustment');
  } else {
    console.log('✅ user_flashcard_reviews table exists');
  }
  
  // Check if flashcard_review_history table exists
  const { data: historyTable, error: historyError } = await supabase
    .from('flashcard_review_history')
    .select('id')
    .limit(1);
  
  if (historyError && historyError.code === '42P01') {
    console.log('❌ flashcard_review_history table does not exist');
    console.log('Please run the SQL script mentioned above');
  } else if (historyError && historyError.code === '42501') {
    console.log('⚠️  flashcard_review_history table exists but RLS policies may need adjustment');
  } else {
    console.log('✅ flashcard_review_history table exists');
  }
  
  // Test inserting a sample review
  console.log('\nTesting table functionality...');
  
  const testUserId = '00000000-0000-0000-0000-000000000000'; // Dummy UUID
  const testFlashcardId = '00000000-0000-0000-0000-000000000001'; // Dummy UUID
  
  try {
    // Try to select from user_flashcard_reviews
    const { data, error } = await supabase
      .from('user_flashcard_reviews')
      .select('*')
      .eq('user_id', testUserId)
      .limit(1);
    
    if (error) {
      if (error.code === '42P01') {
        console.log('❌ Tables need to be created. Please run the SQL script in Supabase dashboard.');
      } else {
        console.log('⚠️  Tables exist but there may be permission issues:', error.message);
      }
    } else {
      console.log('✅ Tables are properly configured and accessible');
    }
  } catch (err) {
    console.error('Error testing tables:', err);
  }
  
  console.log('\n========================================');
  console.log('NEXT STEPS:');
  console.log('1. Go to your Supabase dashboard');
  console.log('2. Navigate to the SQL Editor');
  console.log('3. Copy and paste the contents of scripts/create_spaced_repetition_tables.sql');
  console.log('4. Run the SQL script');
  console.log('5. Verify the tables were created in the Table Editor');
  console.log('========================================');
}

checkAndCreateTables();