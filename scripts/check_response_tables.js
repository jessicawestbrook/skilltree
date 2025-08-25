const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkTableUsage() {
  const tables = [
    'question_responses',
    'assessment_question_responses', 
    'user_test_responses',
    'user_question_attempts'
  ];
  
  console.log('Checking response tables...\n');
  
  for (const table of tables) {
    try {
      const { count, error } = await supabase
        .from(table)
        .select('*', { count: 'exact', head: true });
      
      if (!error) {
        console.log(`${table}: ${count || 0} rows`);
        
        // Get sample column names if table has data
        if (count > 0) {
          const { data: sample } = await supabase
            .from(table)
            .select('*')
            .limit(1);
          
          if (sample && sample.length > 0) {
            console.log(`  Columns: ${Object.keys(sample[0]).join(', ')}`);
          }
        }
      } else {
        console.log(`${table}: Error - ${error.message}`);
      }
    } catch (e) {
      console.log(`${table}: Error accessing - ${e.message}`);
    }
    console.log('');
  }
}

checkTableUsage();