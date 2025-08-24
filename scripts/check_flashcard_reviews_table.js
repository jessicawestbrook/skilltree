const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkTableStructure() {
  console.log('Checking user_flashcard_reviews table structure...\n');

  // Test inserting a minimal record to see what columns are accepted
  const testData = {
    user_id: '00000000-0000-0000-0000-000000000000',
    flashcard_id: 'test-id',
    flashcard_type: 'vocabulary',
    last_reviewed: new Date().toISOString(),
    next_review: new Date().toISOString(),
    review_count: 0,
    easiness_factor: 2.5,
    interval_days: 1
  };

  console.log('Testing with minimal data (no consecutive_correct)...');
  const { data: result1, error: error1 } = await supabase
    .from('user_flashcard_reviews')
    .insert(testData)
    .select();

  if (error1) {
    console.log('Error with minimal insert:', error1.message);
  } else {
    console.log('Success! Table accepts these columns:', Object.keys(testData));
    // Clean up
    if (result1 && result1[0]) {
      await supabase
        .from('user_flashcard_reviews')
        .delete()
        .eq('id', result1[0].id);
    }
  }

  // Now test with consecutive_correct
  console.log('\nTesting with consecutive_correct column...');
  const testDataWithCC = {
    ...testData,
    consecutive_correct: 0
  };

  const { data: result2, error: error2 } = await supabase
    .from('user_flashcard_reviews')
    .insert(testDataWithCC)
    .select();

  if (error2) {
    console.log('Error with consecutive_correct:', error2.message);
    console.log('This column does not exist in the table');
  } else {
    console.log('Success! consecutive_correct column exists');
    // Clean up
    if (result2 && result2[0]) {
      await supabase
        .from('user_flashcard_reviews')
        .delete()
        .eq('id', result2[0].id);
    }
  }

  // Test other potentially missing columns
  console.log('\nTesting other columns...');
  const fullTestData = {
    ...testData,
    total_correct: 0,
    total_attempts: 0,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  const { data: result3, error: error3 } = await supabase
    .from('user_flashcard_reviews')
    .insert(fullTestData)
    .select();

  if (error3) {
    console.log('Error with additional columns:', error3.message);
    console.log('Some columns may be missing');
  } else {
    console.log('Success! All standard columns exist');
    // Clean up
    if (result3 && result3[0]) {
      await supabase
        .from('user_flashcard_reviews')
        .delete()
        .eq('id', result3[0].id);
    }
  }

  console.log('\n✅ Table check complete');
}

checkTableStructure().catch(console.error);