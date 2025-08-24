const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function testAssessmentDirect() {
  console.log('Testing assessment functionality directly...\n');
  
  // Get a test user
  const { data: users } = await supabase
    .from('profiles')
    .select('user_id')
    .limit(1);
  
  if (!users || users.length === 0) {
    console.log('No users found in database.');
    return;
  }
  
  const testUserId = users[0].user_id;
  console.log('Test User ID:', testUserId);
  
  // Find a category with questions
  const { data: questionsWithCategories } = await supabase
    .from('questions')
    .select('skill_id')
    .limit(10);
  
  if (!questionsWithCategories || questionsWithCategories.length === 0) {
    console.log('No questions found in database.');
    return;
  }
  
  const categoryId = questionsWithCategories[0].skill_id;
  
  // Get category info
  const { data: category } = await supabase
    .from('skill_tree_nodes')
    .select('name')
    .eq('id', categoryId)
    .single();
  
  console.log('Test Category:', category?.name || 'Unknown');
  console.log('Category ID:', categoryId);
  
  // Test creating an assessment session
  console.log('\nAttempting to create assessment session...');
  
  const { data: attempt, error: attemptError } = await supabase
    .from('user_test_attempts')
    .insert({
      user_id: testUserId,
      test_id: categoryId, // Using category_id as test_id
      attempt_number: 1,
      is_practice: true,
      raw_score: 0,
      scaled_score: 0,
      time_taken_seconds: 0,
      is_completed: false,
      metadata: {
        session_type: 'practice',
        confidence_interval: 1,
        streak_count: 0,
        max_streak: 0,
        total_questions: 0,
        correct_answers: 0,
        category_id: categoryId
      }
    })
    .select()
    .single();
  
  if (attemptError) {
    console.error('❌ Error creating assessment:', attemptError.message);
    console.error('Error details:', attemptError);
  } else {
    console.log('✅ Assessment session created successfully!');
    console.log('Session ID:', attempt.id);
    console.log('Session data:', JSON.stringify(attempt, null, 2));
    
    // Clean up test data
    const { error: deleteError } = await supabase
      .from('user_test_attempts')
      .delete()
      .eq('id', attempt.id);
    
    if (deleteError) {
      console.error('Error cleaning up test data:', deleteError);
    } else {
      console.log('\n✅ Test data cleaned up successfully.');
    }
  }
  
  console.log('\n✅ Direct assessment test completed.');
}

testAssessmentDirect().catch(console.error);