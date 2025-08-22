const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

// Use service role key for admin operations
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function verifyUpdates() {
  try {
    // Check specific words that were reported as updated
    const testWords = ['vlogging', 'toastmaster', 'vocabulary', 'volcano'];
    
    console.log('Checking pronunciation updates...');
    
    for (const word of testWords) {
      const { data, error } = await supabase
        .from('spelling_words')
        .select('word, pronunciation_guide')
        .eq('word', word)
        .single();
        
      if (error) {
        console.log(`Error checking ${word}:`, error);
      } else if (data) {
        console.log(`${data.word}: ${data.pronunciation_guide || 'MISSING'}`);
      } else {
        console.log(`${word}: NOT FOUND`);
      }
    }
    
    // Count total words missing pronunciation
    const { data: missingCount, error: countError } = await supabase
      .from('spelling_words')
      .select('id', { count: 'exact' })
      .is('pronunciation_guide', null);
      
    if (!countError) {
      console.log(`\nTotal words still missing pronunciation: ${missingCount.length}`);
    }
    
  } catch (error) {
    console.error('Verification failed:', error);
  }
}

verifyUpdates();