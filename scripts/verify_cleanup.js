const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyCleanup() {
  console.log('Verifying cleanup...\n');
  
  // Check that old tables are gone
  const oldTables = [
    'question_responses',
    'assessment_question_responses',
    'user_test_responses',
    'user_question_attempts'
  ];
  
  for (const table of oldTables) {
    const { error } = await supabase
      .from(table)
      .select('*', { count: 'exact', head: true });
    
    if (error && error.code === '42P01') {
      console.log('✅', table, '- Successfully dropped');
    } else if (!error) {
      console.log('⚠️', table, '- Still exists!');
    } else {
      console.log('?', table, '- Unknown status:', error.message);
    }
  }
  
  // Verify unified table exists
  console.log('\nUnified table status:');
  const { count, error: unifiedError } = await supabase
    .from('user_question_responses')
    .select('*', { count: 'exact', head: true });
  
  if (!unifiedError) {
    console.log('✅ user_question_responses - Exists with', count || 0, 'rows');
  } else {
    console.log('❌ user_question_responses - Error:', unifiedError.message);
  }
}

verifyCleanup();