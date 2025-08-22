// Check existing data structure in spelling_words table
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

async function checkExistingData() {
  try {
    console.log('🔍 Checking existing data in spelling_words table...');
    
    // Get a few existing records to see the data structure
    const { data: existingData, error } = await supabase
      .from('spelling_words')
      .select('*')
      .limit(3);
    
    if (error) {
      console.error('Error querying existing data:', error.message);
      return;
    }
    
    if (existingData && existingData.length > 0) {
      console.log('\n📊 Existing data structure:');
      console.log('Number of existing records:', existingData.length);
      console.log('\nSample record:');
      console.log(JSON.stringify(existingData[0], null, 2));
      
      console.log('\n🔧 Field types detected:');
      Object.keys(existingData[0]).forEach(key => {
        const value = existingData[0][key];
        const type = typeof value;
        const isArray = Array.isArray(value);
        console.log(`  ${key}: ${isArray ? 'array' : type} - ${JSON.stringify(value)}`);
      });
    } else {
      console.log('✅ Table is empty, no existing data structure to match');
    }
    
    // Get count
    const { count, error: countError } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });
    
    if (!countError) {
      console.log(`\n📈 Total records in table: ${count}`);
    }
    
  } catch (err) {
    console.error('Unexpected error:', err.message);
  }
}

checkExistingData();