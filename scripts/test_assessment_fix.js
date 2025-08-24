const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function testAssessmentFix() {
  console.log('Testing assessment fix...\n');
  
  // Get a real user and category for testing
  const { data: user } = await supabase.auth.getUser();
  
  if (!user?.user) {
    console.log('No authenticated user found. Please log in to test assessments.');
    return;
  }
  
  console.log('User ID:', user.user.id);
  
  // Get a category with questions
  const { data: categories } = await supabase
    .from('skill_tree_nodes')
    .select('id, name')
    .limit(5);
  
  console.log('\nAvailable categories:');
  categories?.forEach(cat => console.log(`- ${cat.name} (${cat.id})`));
  
  // Check if any category has questions
  for (const category of categories || []) {
    const { data: questions, error } = await supabase
      .from('questions')
      .select('id')
      .eq('skill_id', category.id)
      .limit(1);
    
    if (questions && questions.length > 0) {
      console.log(`\nCategory "${category.name}" has questions available.`);
      console.log('Testing assessment creation for this category...');
      
      // Try to create an assessment session
      const { data: attempt, error: attemptError } = await supabase
        .from('user_test_attempts')
        .insert({
          user_id: user.user.id,
          test_id: category.id,
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
            category_id: category.id
          }
        })
        .select()
        .single();
      
      if (attemptError) {
        console.error('Error creating assessment:', attemptError);
      } else {
        console.log('✅ Assessment session created successfully!');
        console.log('Session ID:', attempt.id);
        
        // Clean up test data
        await supabase
          .from('user_test_attempts')
          .delete()
          .eq('id', attempt.id);
        console.log('Test data cleaned up.');
      }
      
      break;
    }
  }
  
  console.log('\n✅ Assessment fix test completed.');
}

testAssessmentFix().catch(console.error);