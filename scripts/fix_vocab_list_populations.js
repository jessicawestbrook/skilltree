const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY // Use service role for admin operations
);

async function fixVocabListPopulations() {
  console.log('Fixing vocabulary list populations to include all words...\n');
  
  const difficultyMappings = [
    { name: 'Foundation Vocabulary', vocabulary_difficulty_id: 1 },
    { name: 'Academic Vocabulary', vocabulary_difficulty_id: 2 },
    { name: 'Sophisticated Vocabulary', vocabulary_difficulty_id: 3 },
    { name: 'Specialized Vocabulary', vocabulary_difficulty_id: 4 },
    { name: 'Scholarly Vocabulary', vocabulary_difficulty_id: 5 }
  ];
  
  for (const mapping of difficultyMappings) {
    console.log(`\nProcessing ${mapping.name}...`);
    
    // Get the study list
    const { data: list, error: listError } = await supabase
      .from('study_lists')
      .select('id, name')
      .eq('name', mapping.name)
      .single();
      
    if (listError || !list) {
      console.error(`Could not find list "${mapping.name}":`, listError);
      continue;
    }
    
    // Get all existing items in this list
    const { data: existingItems, error: existingError } = await supabase
      .from('study_list_items')
      .select('item_id')
      .eq('study_list_id', list.id)
      .eq('item_type', 'spelling_word');
      
    if (existingError) {
      console.error(`Error fetching existing items:`, existingError);
      continue;
    }
    
    const existingIds = new Set(existingItems?.map(item => item.item_id) || []);
    console.log(`Currently has ${existingIds.size} items`);
    
    // Get ALL words for this difficulty level (no limit)
    let allWords = [];
    let offset = 0;
    const batchSize = 1000;
    
    while (true) {
      const { data: words, error: wordsError } = await supabase
        .from('spelling_words')
        .select('id')
        .eq('is_vocabulary_word', true)
        .eq('vocabulary_difficulty_id', mapping.vocabulary_difficulty_id)
        .range(offset, offset + batchSize - 1);
        
      if (wordsError) {
        console.error(`Error fetching words batch at offset ${offset}:`, wordsError);
        break;
      }
      
      if (!words || words.length === 0) {
        break;
      }
      
      allWords = allWords.concat(words);
      
      if (words.length < batchSize) {
        break;
      }
      
      offset += batchSize;
    }
    
    console.log(`Found ${allWords.length} total words for difficulty ${mapping.vocabulary_difficulty_id}`);
    
    // Find words that need to be added
    const wordsToAdd = allWords.filter(word => !existingIds.has(word.id));
    
    if (wordsToAdd.length > 0) {
      console.log(`Need to add ${wordsToAdd.length} missing words`);
      
      // Prepare items for batch insert
      const items = wordsToAdd.map(word => ({
        study_list_id: list.id,
        item_type: 'spelling_word',
        item_id: word.id
      }));
      
      // Insert in batches of 100
      let successCount = 0;
      for (let i = 0; i < items.length; i += 100) {
        const batch = items.slice(i, i + 100);
        const { error: insertError } = await supabase
          .from('study_list_items')
          .insert(batch);
          
        if (insertError) {
          console.error(`Error inserting batch ${Math.floor(i/100) + 1}:`, insertError);
        } else {
          successCount += batch.length;
          if ((i + 100) % 500 === 0) {
            console.log(`  Progress: ${Math.min(i + 100, items.length)}/${items.length} words added`);
          }
        }
      }
      
      console.log(`Successfully added ${successCount} words to ${mapping.name}`);
    } else {
      console.log(`List is already complete`);
    }
  }
  
  // Show final statistics
  console.log('\n=== Final Vocabulary Difficulty List Statistics ===');
  for (const mapping of difficultyMappings) {
    const { data: list } = await supabase
      .from('study_lists')
      .select('id')
      .eq('name', mapping.name)
      .single();
      
    if (list) {
      const { count, error } = await supabase
        .from('study_list_items')
        .select('*', { count: 'exact', head: true })
        .eq('study_list_id', list.id);
        
      if (!error) {
        console.log(`${mapping.name}: ${count} words`);
      }
    }
  }
}

fixVocabListPopulations()
  .then(() => console.log('\nDone!'))
  .catch(console.error);