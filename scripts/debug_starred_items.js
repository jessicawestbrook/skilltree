const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function debugStarredItems() {
  console.log('Debugging Starred Items\n');
  console.log('=' .repeat(50));

  try {
    // Check what's in starred_items
    console.log('\n1. Checking starred_items table...');
    const { data: starredItems, error: starredError } = await supabase
      .from('starred_items')
      .select('*')
      .limit(10);

    if (starredError) {
      console.error('Error fetching starred_items:', starredError);
      return;
    }

    console.log(`Found ${starredItems?.length || 0} starred items:`);
    starredItems?.forEach(item => {
      console.log(`  - Type: ${item.item_type}, ID: ${item.item_id}`);
      if (item.item_data) {
        console.log(`    Data: ${JSON.stringify(item.item_data).substring(0, 100)}...`);
      }
    });

    // Try to fetch the specific item causing the error
    const problemId = '9c052740-39a8-4206-9a32-7c05c59a32f2';
    console.log(`\n2. Looking for item with ID: ${problemId}`);
    
    // Check if it's in starred_items
    const { data: specificItem, error: specificError } = await supabase
      .from('starred_items')
      .select('*')
      .eq('item_id', problemId)
      .single();

    if (specificError) {
      console.log('Item not found in starred_items:', specificError.message);
    } else if (specificItem) {
      console.log('Found starred item:', {
        type: specificItem.item_type,
        id: specificItem.item_id,
        data: specificItem.item_data
      });
    }

    // Check if it exists in spelling_words
    console.log('\n3. Checking if ID exists in spelling_words...');
    const { data: spellingWord, error: spellingError } = await supabase
      .from('spelling_words')
      .select('id, word')
      .eq('id', problemId)
      .single();

    if (spellingError) {
      console.log('Not found in spelling_words:', spellingError.message);
    } else if (spellingWord) {
      console.log('Found in spelling_words:', spellingWord);
    }

    // Check table structure
    console.log('\n4. Checking spelling_words table structure...');
    const { data: sampleWord, error: sampleError } = await supabase
      .from('spelling_words')
      .select('*')
      .limit(1)
      .single();

    if (sampleError) {
      console.error('Error fetching sample word:', sampleError);
    } else if (sampleWord) {
      console.log('Sample word columns:', Object.keys(sampleWord));
    }

  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

debugStarredItems();