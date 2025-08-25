const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function populateScrippsLists() {
  console.log('Populating Scripps study lists with words...\n');
  
  // Get the Scripps lists
  const { data: scrippsLists } = await supabase
    .from('study_lists')
    .select('id, name')
    .ilike('name', '%Scripps%')
    .order('name');
    
  if (!scrippsLists || scrippsLists.length === 0) {
    console.error('No Scripps lists found!');
    return;
  }
  
  for (const list of scrippsLists) {
    console.log(`Processing ${list.name}...`);
    
    // Determine the source difficulty for this list
    let sourceDifficulty;
    if (list.name.includes('One Bee')) {
      sourceDifficulty = 'One Bee';
    } else if (list.name.includes('Two Bee')) {
      sourceDifficulty = 'Two Bee';
    } else if (list.name.includes('Three Bee')) {
      sourceDifficulty = 'Three Bee';
    } else {
      console.log(`  - Skipping unknown list: ${list.name}`);
      continue;
    }
    
    // Get all words for this difficulty level
    const { data: words, error: wordsError } = await supabase
      .from('spelling_words')
      .select('id')
      .ilike('original_source', '%Scripps%')
      .ilike('source_difficulty', `%${sourceDifficulty}%`);
      
    if (wordsError) {
      console.error(`  - Error fetching words:`, wordsError);
      continue;
    }
    
    console.log(`  - Found ${words.length} words for ${list.name}`);
    
    if (words.length === 0) {
      console.log(`  - No words found, skipping...`);
      continue;
    }
    
    // Delete existing items for this list (if any)
    const { error: deleteError } = await supabase
      .from('study_list_items')
      .delete()
      .eq('study_list_id', list.id);
      
    if (deleteError) {
      console.error(`  - Error deleting existing items:`, deleteError);
    }
    
    // Create study list items in batches
    const batchSize = 500;
    let totalInserted = 0;
    
    for (let i = 0; i < words.length; i += batchSize) {
      const batch = words.slice(i, i + batchSize);
      const items = batch.map(word => ({
        study_list_id: list.id,
        item_type: 'spelling_word',
        item_id: word.id,
        added_at: new Date().toISOString()
      }));
      
      const { error: insertError } = await supabase
        .from('study_list_items')
        .insert(items);
        
      if (insertError) {
        console.error(`  - Error inserting batch ${Math.floor(i / batchSize) + 1}:`, insertError);
      } else {
        totalInserted += batch.length;
        console.log(`  - Inserted batch ${Math.floor(i / batchSize) + 1}: ${totalInserted}/${words.length} words`);
      }
    }
    
    console.log(`  - Completed ${list.name}: ${totalInserted} words added\n`);
  }
  
  // Get final counts for each list
  console.log('\nFinal word counts for each list:');
  for (const list of scrippsLists || []) {
    const { count } = await supabase
      .from('study_list_items')
      .select('*', { count: 'exact', head: true })
      .eq('study_list_id', list.id);
      
    console.log(`  - ${list.name}: ${count.toLocaleString()} words`);
  }
}

populateScrippsLists().catch(console.error);