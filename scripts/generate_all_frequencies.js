// Export all words from database to process with Python
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function exportWords() {
  console.log('Exporting all words from database...');
  
  // Get all words with their IDs
  const { data, error } = await supabase
    .from('spelling_words')
    .select('id, word')
    .order('word');
    
  if (error) {
    console.error('Error fetching words:', error);
    return;
  }
  
  console.log(`Found ${data.length} words`);
  
  // Save to JSON for Python processing
  fs.writeFileSync('all_words.json', JSON.stringify(data, null, 2));
  console.log('Words exported to all_words.json');
  
  // Also create a simple word list
  const wordList = data.map(w => w.word).join('\n');
  fs.writeFileSync('word_list.txt', wordList);
  console.log('Word list exported to word_list.txt');
}

exportWords();