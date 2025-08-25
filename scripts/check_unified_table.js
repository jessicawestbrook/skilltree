const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkUnifiedTable() {
  const { count, error } = await supabase
    .from('user_question_responses')
    .select('*', { count: 'exact', head: true });
  
  if (!error) {
    console.log('user_question_responses table exists with', count || 0, 'rows');
    
    // Get column info
    const { data: sample } = await supabase
      .from('user_question_responses')
      .select('*')
      .limit(1);
    
    if (sample && sample.length > 0) {
      console.log('Columns:', Object.keys(sample[0]).join(', '));
    } else {
      // Get schema info even if no data
      const { data: columns } = await supabase.rpc('get_table_columns', {
        table_name: 'user_question_responses'
      }).single();
      
      if (columns) {
        console.log('Table exists but is empty');
      }
    }
  } else {
    console.log('user_question_responses table does not exist:', error.message);
  }
}

checkUnifiedTable();