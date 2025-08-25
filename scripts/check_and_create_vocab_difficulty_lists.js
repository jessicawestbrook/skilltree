const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkAndCreateVocabDifficultyLists() {
  console.log('Checking existing vocabulary study lists...\n');
  
  // First, check what vocabulary-related lists exist
  const { data: existingLists, error: fetchError } = await supabase
    .from('study_lists')
    .select('id, name, description, is_public')
    .or('name.ilike.%vocab%,name.ilike.%vocabulary%')
    .order('name');
    
  if (fetchError) {
    console.error('Error fetching lists:', fetchError);
    return;
  }
  
  console.log(`Found ${existingLists.length} vocabulary-related lists:`);
  existingLists.forEach(list => {
    console.log(`- ${list.name} (${list.is_public ? 'public' : 'private'})`);
  });
  
  // Check if we have the vocabulary difficulty lists
  const difficultyNames = [
    'Foundation Vocabulary',
    'Academic Vocabulary', 
    'Sophisticated Vocabulary',
    'Specialized Vocabulary',
    'Scholarly Vocabulary'
  ];
  
  const existingDifficultyLists = existingLists.filter(list => 
    difficultyNames.some(name => list.name === name)
  );
  
  console.log(`\nFound ${existingDifficultyLists.length} vocabulary difficulty lists.`);
  
  if (existingDifficultyLists.length < 5) {
    console.log('\nCreating missing vocabulary difficulty study lists...\n');
    
    const listsToCreate = [
      {
        name: 'Foundation Vocabulary',
        description: 'Basic everyday concepts - Essential words for daily communication',
        vocabulary_difficulty_id: 1
      },
      {
        name: 'Academic Vocabulary',
        description: 'School-level vocabulary - Words commonly used in educational settings',
        vocabulary_difficulty_id: 2
      },
      {
        name: 'Sophisticated Vocabulary',
        description: 'Advanced academic and professional - Complex words for formal writing and speaking',
        vocabulary_difficulty_id: 3
      },
      {
        name: 'Specialized Vocabulary',
        description: 'Domain-specific terminology - Technical words from specific fields',
        vocabulary_difficulty_id: 4
      },
      {
        name: 'Scholarly Vocabulary',
        description: 'Research and expert-level - Advanced words used in academic research and scholarly discourse',
        vocabulary_difficulty_id: 5
      }
    ];
    
    for (const listData of listsToCreate) {
      // Check if this list already exists
      const exists = existingLists.some(list => list.name === listData.name);
      if (exists) {
        console.log(`List "${listData.name}" already exists, skipping...`);
        continue;
      }
      
      // Create the study list (using the same user_id as existing public lists)
      const { data: newList, error: createError } = await supabase
        .from('study_lists')
        .insert({
          user_id: '2eaf6609-b02d-4d15-8b6d-197056945e31', // Same user as Grade vocabulary lists
          name: listData.name,
          description: listData.description,
          is_public: true,
          created_at: new Date().toISOString()
        })
        .select()
        .single();
        
      if (createError) {
        console.error(`Error creating list "${listData.name}":`, createError);
        continue;
      }
      
      console.log(`Created study list: ${listData.name}`);
      
      // Now add vocabulary words to this list based on difficulty
      const { data: words, error: wordsError } = await supabase
        .from('spelling_words')
        .select('id, word')
        .eq('is_vocabulary_word', true)
        .eq('vocabulary_difficulty_id', listData.vocabulary_difficulty_id)
        .limit(1000);
        
      if (wordsError) {
        console.error(`Error fetching words for difficulty ${listData.vocabulary_difficulty_id}:`, wordsError);
        continue;
      }
      
      if (words && words.length > 0) {
        console.log(`Adding ${words.length} words to ${listData.name}...`);
        
        // Prepare items for batch insert
        const items = words.map(word => ({
          study_list_id: newList.id,
          item_type: 'spelling_word',
          item_id: word.id
        }));
        
        // Insert in batches of 100
        for (let i = 0; i < items.length; i += 100) {
          const batch = items.slice(i, i + 100);
          const { error: insertError } = await supabase
            .from('study_list_items')
            .insert(batch);
            
          if (insertError) {
            console.error(`Error inserting batch ${i/100 + 1}:`, insertError);
          }
        }
        
        console.log(`Added ${words.length} words to ${listData.name}`);
      }
    }
    
    console.log('\nFinished creating vocabulary difficulty lists!');
  } else {
    console.log('\nAll vocabulary difficulty lists already exist.');
  }
  
  // Check the counts for each difficulty list
  console.log('\n=== Vocabulary Difficulty List Statistics ===');
  for (const list of existingDifficultyLists) {
    const { count, error } = await supabase
      .from('study_list_items')
      .select('*', { count: 'exact', head: true })
      .eq('study_list_id', list.id);
      
    if (!error) {
      console.log(`${list.name}: ${count} words`);
    }
  }
}

checkAndCreateVocabDifficultyLists()
  .then(() => console.log('\nDone!'))
  .catch(console.error);