const { createClient } = require('@supabase/supabase-js');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env.local') });
const fs = require('fs');

// Read the JSON file
const data = JSON.parse(fs.readFileSync('nlp_parts_of_speech.json', 'utf8'));

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing required environment variables');
  console.log('SUPABASE_URL:', supabaseUrl ? 'Found' : 'Missing');
  console.log('SERVICE_ROLE_KEY:', supabaseKey ? 'Found' : 'Missing');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function applyUpdates() {
  console.log('Applying parts of speech from saved file...');
  console.log('Total words to update:', data.results.length);
  
  let successCount = 0;
  let errorCount = 0;
  const errors = [];
  
  // Test with just one word first
  console.log('\nTesting with first word...');
  const testItem = data.results[0];
  console.log(`Updating "${testItem.word}" (ID: ${testItem.id}) to part_of_speech: "${testItem.part_of_speech}"`);
  
  const { data: testResult, error: testError } = await supabase
    .from('spelling_words')
    .update({ part_of_speech: testItem.part_of_speech })
    .eq('id', testItem.id)
    .select();
  
  if (testError) {
    console.log('Test update failed:', testError);
    console.log('Full error details:', JSON.stringify(testError, null, 2));
    return;
  } else {
    console.log('Test update succeeded:', testResult);
  }
  
  // Process in smaller batches
  const batchSize = 50;
  for (let i = 0; i < data.results.length; i += batchSize) {
    const batch = data.results.slice(i, i + batchSize);
    
    for (const item of batch) {
      const { error } = await supabase
        .from('spelling_words')
        .update({ part_of_speech: item.part_of_speech })
        .eq('id', item.id);
      
      if (error) {
        errorCount++;
        if (errors.length < 5) {
          errors.push({ word: item.word, id: item.id, error: error.message, code: error.code });
        }
      } else {
        successCount++;
      }
    }
    
    if ((i + batchSize) % 500 === 0 || i + batchSize >= data.results.length) {
      const progress = Math.min(i + batchSize, data.results.length);
      console.log(`Progress: ${progress}/${data.results.length} - Success: ${successCount}, Errors: ${errorCount}`);
    }
  }
  
  console.log('\nFinal results:');
  console.log('Successfully updated:', successCount);
  console.log('Errors:', errorCount);
  
  if (errors.length > 0) {
    console.log('\nSample errors:');
    errors.forEach(e => console.log(`  ${e.word}: ${e.error}`));
  }
  
  // Verify the updates
  const { count } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .not('part_of_speech', 'is', null);
    
  console.log('\nTotal words with part_of_speech in database:', count);
}

applyUpdates().catch(console.error);