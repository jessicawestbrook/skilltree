const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkTableStructure() {
  try {
    console.log('Checking user_module_progress table structure...\n');
    
    // Get a sample row to see actual columns
    const { data, error } = await supabase
      .from('user_module_progress')
      .select('*')
      .limit(1);
    
    if (error) {
      console.log('Error querying table:', error);
    } else if (data && data.length > 0) {
      console.log('Actual columns in user_module_progress:');
      console.log(Object.keys(data[0]));
      console.log('\nSample data:', data[0]);
    } else {
      console.log('Table exists but is empty');
      
      // Try to get column info another way
      const { data: emptyQuery, error: emptyError } = await supabase
        .from('user_module_progress')
        .select('*')
        .eq('id', 'non-existent-id');
      
      console.log('Query succeeded, table structure is accessible');
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('REQUIRED FIXES:');
    console.log('='.repeat(50));
    console.log('\n1. Add missing columns to user_module_progress:');
    console.log('   - status (for tracking progress state)');
    console.log('   - updated_at (for ordering)');
    console.log('\n2. Fix ProfilePage.tsx to use correct column names');
    console.log('\n3. Remove invalid vocab- prefixed IDs from queries');
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkTableStructure();