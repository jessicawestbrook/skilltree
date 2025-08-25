const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkTables() {
  try {
    console.log('=== CHECKING RELATED TABLES ===\n');
    
    // Check if spelling_difficulty table exists
    console.log('1. Checking for spelling_difficulty table...');
    const { data: spellingDiff, error: spellingError } = await supabase
      .from('spelling_difficulty')
      .select('*')
      .limit(1);
    
    if (spellingError) {
      console.log('❌ spelling_difficulty table does not exist or is not accessible');
      console.log('   Error:', spellingError.message);
    } else {
      console.log('✓ spelling_difficulty table exists');
      if (spellingDiff && spellingDiff.length > 0) {
        console.log('  Sample data:', spellingDiff[0]);
      }
    }
    
    // Check if vocabulary_difficulty table exists
    console.log('\n2. Checking for vocabulary_difficulty table...');
    const { data: vocabDiff, error: vocabError } = await supabase
      .from('vocabulary_difficulty')
      .select('*')
      .limit(1);
    
    if (vocabError) {
      console.log('❌ vocabulary_difficulty table does not exist or is not accessible');
      console.log('   Error:', vocabError.message);
    } else {
      console.log('✓ vocabulary_difficulty table exists');
      if (vocabDiff && vocabDiff.length > 0) {
        console.log('  Sample data:', vocabDiff[0]);
      }
    }
    
    // Check the current view structure
    console.log('\n3. Checking current spelling_words_with_sources view...');
    const { data: viewData, error: viewError } = await supabase
      .from('spelling_words_with_sources')
      .select('*')
      .limit(1);
    
    if (viewError) {
      console.log('View error:', viewError.message);
    } else if (viewData && viewData.length > 0) {
      console.log('View has these fields:');
      Object.keys(viewData[0]).forEach(field => {
        console.log(`  - ${field}`);
      });
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkTables();