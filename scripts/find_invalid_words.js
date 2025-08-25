const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function searchInvalidWords() {
  console.log('Searching for words with "valid word" in definition...');
  console.log('='.repeat(60));
  
  // Search for 'valid word' in definitions
  const { data, error } = await supabase
    .from('spelling_words')
    .select('id, word, definition')
    .ilike('definition', '%valid word%')
    .order('word');
  
  if (error) {
    console.log('Error:', error);
    return;
  }
  
  console.log(`Found ${data.length} entries with "valid word" in definition:\n`);
  
  data.forEach((entry, index) => {
    console.log(`${index + 1}. Word: ${entry.word}`);
    console.log(`   ID: ${entry.id}`);
    console.log(`   Definition: ${entry.definition}`);
    console.log(`   Issue: Likely invalid or combined words`);
    console.log('-'.repeat(60));
  });
  
  // Also check for other common patterns that indicate invalid entries
  console.log('\nChecking for other potential issues...');
  
  // Check for entries that might be combined words (looking for unusual patterns)
  const { data: suspicious, error: suspiciousError } = await supabase
    .from('spelling_words')
    .select('id, word, definition')
    .or('definition.is.null,definition.eq.')
    .limit(20);
    
  if (!suspiciousError && suspicious && suspicious.length > 0) {
    console.log(`\nFound ${suspicious.length} entries with empty definitions:`);
    suspicious.forEach((entry, index) => {
      console.log(`${index + 1}. Word: ${entry.word} (ID: ${entry.id})`);
    });
  }
  
  // Check for entries that look like multiple words concatenated
  console.log('\nChecking for concatenated words...');
  const { data: allWords, error: allError } = await supabase
    .from('spelling_words')
    .select('id, word')
    .limit(10000);
    
  if (!allError && allWords) {
    const concatenated = allWords.filter(entry => {
      // Check if word looks like multiple words stuck together
      // (has capital letters in the middle or unusual patterns)
      const word = entry.word;
      return /[a-z][A-Z]/.test(word) || // lowercase followed by uppercase
             word.length > 20 && !/[-\s]/.test(word); // very long word without hyphens or spaces
    });
    
    if (concatenated.length > 0) {
      console.log(`\nFound ${concatenated.length} potentially concatenated words:`);
      concatenated.slice(0, 20).forEach((entry, index) => {
        console.log(`${index + 1}. Word: ${entry.word} (ID: ${entry.id})`);
      });
    }
  }
  
  console.log(`\nTotal problematic entries found: ${data.length + (suspicious?.length || 0)}`);
  
  // Save results to a file for review
  const results = {
    invalidDefinitions: data,
    emptyDefinitions: suspicious || [],
    timestamp: new Date().toISOString()
  };
  
  const fs = require('fs');
  fs.writeFileSync('scripts/invalid_words_report.json', JSON.stringify(results, null, 2));
  console.log('\nFull report saved to scripts/invalid_words_report.json');
}

searchInvalidWords().catch(console.error);