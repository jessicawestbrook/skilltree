const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkSchema() {
  try {
    // Get a sample question to see the structure
    const { data: sampleQuestion, error } = await supabase
      .from('questions')
      .select('*')
      .limit(1);
    
    if (error) throw error;
    
    if (sampleQuestion && sampleQuestion.length > 0) {
      console.log('Questions table structure:');
      console.log('Columns:', Object.keys(sampleQuestion[0]));
      console.log('\nSample question:', JSON.stringify(sampleQuestion[0], null, 2));
    } else {
      console.log('No questions found in the table');
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkSchema();