const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function populateVocabDifficultyLists() {
  console.log('Populating vocabulary difficulty study lists with words...\n');
  
  const difficultyMappings = [
    { name: 'Foundation Vocabulary', vocabulary_difficulty_id: 1 },
    { name: 'Academic Vocabulary', vocabulary_difficulty_id: 2 },
    { name: 'Sophisticated Vocabulary', vocabulary_difficulty_id: 3 },
    { name: 'Specialized Vocabulary', vocabulary_difficulty_id: 4 },
    { name: 'Scholarly Vocabulary', vocabulary_difficulty_id: 5 }
  ];
  
  for (const mapping of difficultyMappings) {
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
    
    // Get words for this difficulty level
    const { data: words, error: wordsError } = await supabase
      .from('spelling_words')
      .select('id, word')
      .eq('is_vocabulary_word', true)
      .eq('vocabulary_difficulty_id', mapping.vocabulary_difficulty_id)
      .limit(1000);
      
    if (wordsError) {
      console.error(`Error fetching words for difficulty ${mapping.vocabulary_difficulty_id}:`, wordsError);
      continue;
    }
    
    if (words && words.length > 0) {
      console.log(`Adding ${words.length} words to ${mapping.name}...`);
      
      // Prepare items for batch insert
      const items = words.map(word => ({
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
        }
      }
      
      console.log(`Successfully added ${successCount} words to ${mapping.name}`);
    } else {
      console.log(`No words found for ${mapping.name} (difficulty ${mapping.vocabulary_difficulty_id})`);
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

populateVocabDifficultyLists()
  .then(() => console.log('\nDone!'))
  .catch(console.error);