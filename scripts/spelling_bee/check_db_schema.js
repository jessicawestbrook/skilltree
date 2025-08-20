// Check the actual database schema for spelling_words table
const { createClient } = require('@supabase/supabase-js');

// Load environment variables
require('dotenv').config({ path: '../../.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function checkSchema() {
  try {
    console.log('Checking spelling_words table schema...');
    
    // Try to query table info from information_schema
    const { data, error } = await supabase
      .rpc('get_table_columns', { table_name: 'spelling_words' })
      .single();
    
    if (error) {
      console.log('RPC failed, trying direct query...');
      
      // Try a simple query to see what columns exist
      const { data: testData, error: testError } = await supabase
        .from('spelling_words')
        .select('*')
        .limit(1);
      
      if (testError) {
        console.error('Table query error:', testError.message);
        
        // Check if table exists at all
        if (testError.message.includes('does not exist')) {
          console.log('❌ Table "spelling_words" does not exist yet');
          console.log('✅ Need to create the table first');
          return;
        }
      } else {
        console.log('✅ Table exists but is empty');
        console.log('Available columns from empty query:', Object.keys(testData?.[0] || {}));
      }
    } else {
      console.log('✅ Table schema:', data);
    }
    
  } catch (err) {
    console.error('Error:', err.message);
  }
}

checkSchema();